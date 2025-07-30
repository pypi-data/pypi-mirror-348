import asyncio
import collections.abc
import contextlib
import functools
import inspect
import time

import typing_extensions as typing

from .sila.utils import clear_interval, set_interval

T = typing.TypeVar("T")


class Subject(typing.Generic[T]):
    """
    An observable that can be updated externally and subscribed to by multiple observers.

    Args:
      maxsize: The maximum number of messages to track in the queue.
      default: The default value to use if no value has been set.
    """

    def __init__(
        self,
        maxsize: int = 0,
        default: typing.Optional[T] = None,
    ) -> None:
        self._maxsize = maxsize
        self._value: typing.Optional[T] = default
        self.subscribers: list[asyncio.Queue[T]] = []
        self._queue_tasks: set[asyncio.Task] = set()
        self._cancellation_tasks: set[asyncio.Task] = set()

    @property
    def current(self) -> typing.Optional[T]:
        """The current value."""
        return self._value

    def add(self) -> asyncio.Queue:
        """Add subscriber that will be notified on change to the current value."""
        queue = asyncio.Queue[T](maxsize=self._maxsize)
        if self._value is not None:
            queue.put_nowait(self._value)

        self.subscribers.append(queue)

        return queue

    def remove(self, subscriber: asyncio.Queue) -> None:
        """Remove a subscriber."""
        self.subscribers.remove(subscriber)

        if not self.subscribers:
            for task in [*self._queue_tasks]:
                task.cancel()
            self._queue_tasks.clear()

    def notify(self) -> None:
        """Propagate updates to the current value to all subscribers."""
        if self._value is not None:
            for subscriber in self.subscribers:
                subscriber.put_nowait(self._value)

    def update(self, value: T) -> None:
        """Update the current value, if `value` is not current value."""
        if self._value != value:
            self._value = value
            self.notify()

    async def get(
        self,
        predicate: typing.Callable[[T], bool] = lambda _: True,
        timeout: typing.Optional[float] = None,
        current: bool = False,
    ) -> T:
        """
        Request an upcoming value that satisfies the `predicate`.

        If used without `timeout` this will block indefinitely until a value satisfies the `predicate`.

        Args:
          predicate: A filter predicate to apply.
          timeout: How many seconds to wait for new value before timing out.
          current: Whether to check the current value against the predicate.

        Raises:
          TimeoutError: If the `timeout` is exceeded.
        """

        if all((current, (value := self.current), predicate(value))):
            return value

        queue = self.add()
        start_time = time.perf_counter()

        try:
            while True:
                wait_for = timeout + start_time - time.perf_counter() if timeout is not None else None

                try:
                    value = await asyncio.wait_for(queue.get(), timeout=wait_for)
                    queue.task_done()
                except (TimeoutError, asyncio.TimeoutError):
                    raise TimeoutError from None

                if predicate(value):
                    return value
        finally:
            self.remove(queue)

    async def subscribe(self, abort: typing.Optional[asyncio.Event] = None) -> typing.AsyncIterator[T]:
        """
        Subscribe to be notified to changes to the current value.

        Args:
          abort: An cancellable event, allowing subscriptions to be terminated.
        """
        queue = self.add()

        abort = abort or asyncio.Event()
        cancellation = asyncio.create_task(abort.wait(), name="subscription-cancellation")
        self._cancellation_tasks.add(cancellation)
        cancellation.add_done_callback(self._cancellation_tasks.discard)

        try:
            while not abort.is_set():
                queue_task = asyncio.create_task(queue.get(), name="subscription-queue")
                self._queue_tasks.add(queue_task)
                queue_task.add_done_callback(self._queue_tasks.discard)

                done, pending = await asyncio.wait((queue_task, cancellation), return_when=asyncio.FIRST_COMPLETED)

                if queue_task in done:
                    value = queue_task.result()
                    yield value

                if cancellation in done:
                    for pending_task in pending:
                        with contextlib.suppress(asyncio.TimeoutError):
                            await asyncio.wait_for(pending_task, 0)
                    break

        except asyncio.CancelledError:
            cancellation.cancel()
        finally:
            cancellation.cancel()
            self.remove(queue)


class Publisher(typing.Generic[T], Subject[T]):
    """
    An observable which updates itself by polling a data source.

    Args:
      source: A function or coroutine that will be called at a fixed interval as the data source of the subscription.
      interval: How many seconds to wait between polling calls to `source`.
      maxsize: The maximum number of messages to track in the queue.

    Examples:
      Subscribe to a publisher which will call `method` every 2 seconds:
      >>> publisher = Publisher[str](maxsize=100, source=method, interval=2)
      >>> async for state in publisher.subscribe():
      >>>     yield state
    """

    def __init__(
        self,
        source: typing.Union[collections.abc.Coroutine[None, None, T], typing.Callable[[], T]],
        interval: float = 5,
        maxsize: int = 0,
    ) -> None:
        super().__init__(maxsize)

        self._update_task: typing.Optional[asyncio.Task] = None
        self._source = source
        self._interval = interval

    def _set(self) -> None:
        """
        Create a background task to poll the data `source` and update the current value.

        Task will be destroyed when all subscriptions to the `Publisher` are removed.
        """
        self._update_task = set_interval(self.__self_update, delay=self._interval)

    async def __self_update(self) -> None:
        if (
            isinstance(self._source, functools.partial) and inspect.iscoroutinefunction(self._source.func)
        ) or inspect.iscoroutinefunction(self._source):
            new_value = await self._source()
        else:
            new_value = self._source()

        self.update(new_value)

    @typing.override
    def add(self) -> asyncio.Queue:
        if not self._update_task:
            self._set()

        return super().add()

    @typing.override
    def remove(self, subscriber: asyncio.Queue) -> None:
        super().remove(subscriber)

        if not self.subscribers and self._update_task:
            clear_interval(self._update_task)
            self._update_task = None
            self._value = None

    @typing.override
    async def subscribe(self, abort: typing.Optional[asyncio.Event] = None) -> typing.AsyncIterator[T]:
        """
        Subscribe to be notified to changes to the current value.

        Args:
          abort: An cancellable event, allowing subscriptions to be terminated.

        Examples:
          Conditionally end a subscription:
          >>> publisher = Publisher[str](maxsize=100, source=method, interval=2)
          >>> abort = asyncio.Event()
          >>> async for state in publisher.subscribe(abort):
          >>>     if state == "done":
          >>>         abort.set()
          >>>     yield state
        """
        if not self._update_task:
            self._set()

        async for value in super().subscribe(abort):
            yield value
