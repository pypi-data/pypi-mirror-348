import asyncio
import typing
import unittest.mock

import pytest

from unitelabs.cdk import Publisher, Subject

DEFAULT_VALUE = "default"
ONE_OP_TIME = 0.01


@pytest.fixture
def create_task() -> typing.Generator[asyncio.Task, None, None]:
    tasks = set()

    def _create_task(
        method: typing.Coroutine[typing.Awaitable, None, None],
    ) -> typing.Generator[asyncio.Task, None, None]:
        name = f"subscription-{method.__name__}"
        print(name)
        task = asyncio.create_task(method, name=name)
        tasks.add(task)
        task.add_done_callback(tasks.discard)

        yield task

        task.cancel()
        tasks.discard(task)

    yield _create_task

    for task in tasks:
        task.cancel()
        tasks.discard(task)


async def redundant_update(subject: Subject[str]) -> None:
    """Update the subject 10x, once per operation time, with redundant updates after the first iteration."""
    for x in range(1, 11):
        if x > 1:
            subject.update(f"update {x - 1}")  # redundant update
        subject.update(f"update {x}")
        await asyncio.sleep(ONE_OP_TIME)


async def bg_cancel(cancel_event: asyncio.Event):
    """Set the cancel event after a delay of ~5 operations."""
    await asyncio.sleep(ONE_OP_TIME * 5)
    cancel_event.set()


class TestSubject_Defaults:
    async def test_should_set_default_value_as_currenth(self):
        subject = Subject[str]()
        assert subject.current is None

    async def test_get_should_timeout(self):
        subject = Subject[str]()
        with pytest.raises(TimeoutError):
            await subject.get(timeout=0.01)

    async def test_should_set_default_maxsize(self):
        subject = Subject[str]()
        sub = subject.add()

        assert sub.maxsize == 0


class TestSubject_Subscribe:
    async def test_should_return_default_if_nothing_queued(self):
        subject = Subject[str](maxsize=10, default=DEFAULT_VALUE)

        async for value in subject.subscribe():
            assert value == DEFAULT_VALUE
            if value == DEFAULT_VALUE:
                return

    async def test_should_only_notify_on_changed_value(self, create_task):
        subject = Subject[str](maxsize=10, default=DEFAULT_VALUE)
        subject.update = unittest.mock.Mock(wraps=subject.update)
        subject.notify = unittest.mock.Mock(wraps=subject.notify)

        update_task = next(create_task(redundant_update(subject)))
        await asyncio.sleep(ONE_OP_TIME * 10 + 0.05)

        assert update_task.done()
        assert subject.update.call_count == 19
        assert subject.notify.call_count == 10

    async def test_should_be_cancellable(self, create_task):
        subject = Subject[str](maxsize=10, default=DEFAULT_VALUE)
        cancel_event = asyncio.Event()

        cancel_task = next(create_task(bg_cancel(cancel_event)))

        async for value in subject.subscribe(cancel_event):
            assert value == DEFAULT_VALUE

        # would never get here if not cancelled
        assert cancel_event.is_set()
        assert cancel_task.done()

    async def test_should_be_cancellable_with_update_task(self, create_task):
        subject = Subject[str](maxsize=10, default=DEFAULT_VALUE)
        cancel_event = asyncio.Event()

        update_task = next(create_task(redundant_update(subject)))
        cancel_task = next(create_task(bg_cancel(cancel_event)))
        # will cancel self after 5 operations
        values = [value async for value in subject.subscribe(cancel_event)]

        assert values == [DEFAULT_VALUE, *[f"update {x}" for x in range(1, 6)]]

        assert cancel_event.is_set()
        assert cancel_task.done()

        # update task is not set on publisher; cleanup
        assert not update_task.cancelled()
        update_task.cancel()
        await asyncio.sleep(0.01)
        assert update_task.done()


class TestSubject_Get:
    async def test_should_return_default_if_nothing_queued(self):
        subject = Subject[str](maxsize=10, default=DEFAULT_VALUE)
        assert await subject.get() == DEFAULT_VALUE

    async def test_should_return_default_if_nothing_queued_with_timeout(self):
        subject = Subject[str](maxsize=10, default=DEFAULT_VALUE)
        assert await subject.get(timeout=0.5) == DEFAULT_VALUE

    async def test_should_timeout_if_nothing_queued_matching_predicate(self):
        subject = Subject[str](maxsize=10, default=DEFAULT_VALUE)
        with pytest.raises(TimeoutError):
            await subject.get(lambda x: x != DEFAULT_VALUE, timeout=0.05)

    async def test_should_return_immediately_if_predicate_matches_current_value(self, create_task):
        subject = Subject[str](maxsize=10, default=DEFAULT_VALUE)
        subject.notify = unittest.mock.Mock(wraps=subject.notify)
        update_task = next(create_task(redundant_update(subject)))

        assert subject.current != await subject.get(lambda x: "update" in x)
        assert subject.current == await subject.get(lambda x: "update" in x, current=True)

        # cleanup
        update_task.cancel()
        await asyncio.sleep(0.01)
        assert update_task.done()


class TestSubject_Update:
    async def test_should_update_current_value(self):
        subject = Subject[str](maxsize=10, default=DEFAULT_VALUE)
        subject.update("new value")
        assert subject.current == "new value"

    async def test_should_not_notify_if_value_is_current(self, create_task):
        subject = Subject[str](maxsize=10, default=DEFAULT_VALUE)
        subject.notify = unittest.mock.Mock(wraps=subject.notify)
        subject.update(DEFAULT_VALUE)
        subject.notify.assert_not_called()


class TestSubject_Add:
    async def test_should_add_subscription(self):
        subject = Subject[str](maxsize=10, default=DEFAULT_VALUE)
        sub = subject.add()
        assert isinstance(sub, asyncio.Queue)
        assert sub in subject.subscribers
        assert await sub.get() == DEFAULT_VALUE


class TestSubject_Remove:
    async def test_should_remove_subscription(self):
        subject = Subject[str](maxsize=10, default=DEFAULT_VALUE)
        sub = subject.add()
        assert sub in subject.subscribers
        subject.remove(sub)
        assert sub not in subject.subscribers

    async def test_should_raise_value_error_on_unknown_subscription(self):
        subject = Subject[str](maxsize=10, default=DEFAULT_VALUE)
        with pytest.raises(ValueError):
            subject.remove(asyncio.Queue())

    async def test_should_raise_value_error_on_twice_removed(self):
        subject = Subject[str](maxsize=10, default=DEFAULT_VALUE)
        sub = subject.add()
        subject.remove(sub)
        with pytest.raises(ValueError):
            subject.remove(sub)


class TestPublisher_Get:
    async def test_should_get_new_value(self):
        mock = unittest.mock.Mock(side_effect=[f"update {i}" for i in range(10)])
        pub = Publisher[str](maxsize=10, source=mock, interval=ONE_OP_TIME)

        for i in range(10):
            # each loop creates a new queue and gets the next value
            assert await pub.get() == f"update {i}"
            assert pub.current is None
            assert mock.call_count == i + 1

    async def test_should_reset_current_value_after_get(self):
        mock = unittest.mock.Mock(side_effect=[f"update {i}" for i in range(10)])
        pub = Publisher[str](maxsize=10, source=mock, interval=ONE_OP_TIME)

        assert pub.current is None
        mock.assert_not_called()

        assert await pub.get() == "update 0"
        assert pub.current is None
        mock.assert_called_once()

    async def test_with_current_should_get_next_value(self):
        mock = unittest.mock.Mock(side_effect=[f"update {i}" for i in range(10)])
        pub = Publisher[str](maxsize=10, source=mock, interval=ONE_OP_TIME)

        # get should wait for first value, as current is None
        mock.assert_not_called()
        assert await pub.get(current=True) == "update 0"
        assert pub.current is None
        mock.assert_called_once()
        mock.reset_mock()

        # get should again wait for next value
        assert await pub.get() == "update 1"
        assert pub.current is None
        mock.assert_called_once()

    async def test_should_return_current_value_if_subscription_exists(self):
        mock = unittest.mock.Mock(side_effect=[f"update {i}" for i in range(10)])
        pub = Publisher[str](maxsize=10, source=mock, interval=ONE_OP_TIME)

        sub = pub.add()

        # current should be None until first value is received, get waits for value
        assert pub.current is None
        assert await pub.get() == "update 0"
        assert pub.current == "update 0"
        mock.assert_called_once()
        mock.reset_mock()

        # current should return last value, without waiting for new value
        assert await pub.get(current=True) == "update 0"
        assert pub.current == await pub.get()
        mock.assert_not_called()

        # cleanup
        pub.remove(sub)
        await asyncio.sleep(0.03)
        assert not pub._update_task


class TestPublisher_Add:
    async def test_should_start_polling_after_add(self):
        mock = unittest.mock.Mock(side_effect=[f"value {i}" for i in range(10)])
        pub = Publisher[str](maxsize=10, source=mock, interval=ONE_OP_TIME)
        pub._set = unittest.mock.Mock(wraps=pub._set)

        assert not pub._update_task
        mock.assert_not_called()

        sub = pub.add()
        pub._set.assert_called_once()
        await asyncio.sleep(ONE_OP_TIME)

        assert sub.qsize() >= 1
        mock.assert_called()
        assert pub._update_task

        pub.remove(sub)

    async def test_should_not_start_polling_again_if_other_subscribers(self):
        pub = Publisher[str](maxsize=10, source=lambda: "value", interval=ONE_OP_TIME)
        pub._set = unittest.mock.Mock(wraps=pub._set)
        assert not pub._update_task

        sub = pub.add()
        assert pub._update_task
        pub._set.assert_called_once()
        pub._set.reset_mock()

        sub2 = pub.add()
        pub._set.assert_not_called()

        for s in [sub, sub2]:
            pub.remove(s)


class TestPublisher_Subscribe:
    async def test_should_create_background_task_if_first_subscriber(self, create_task):
        mock = unittest.mock.Mock(side_effect=[f"value {i}" for i in range(10)])
        pub = Publisher[str](maxsize=10, source=mock, interval=ONE_OP_TIME)
        pub._set = unittest.mock.Mock(wraps=pub._set)
        assert not pub._update_task

        cancel_event = asyncio.Event()
        cancel_task = next(create_task(bg_cancel(cancel_event)))
        mock_call_count = 0
        async for _ in pub.subscribe(abort=cancel_event):
            assert pub._update_task
            mock_call_count += 1
            assert mock.call_count == mock_call_count

        # await asyncio.sleep(ONE_OP_TIME * 5)
        pub._set.assert_called_once()
        assert not pub._update_task
        assert cancel_task.done()

    async def test_should_not_create_second_background_task_on_subscription(self, create_task):
        mock = unittest.mock.Mock(side_effect=[f"value {i}" for i in range(10)])

        pub = Publisher[str](maxsize=10, source=mock, interval=ONE_OP_TIME)
        pub._set = unittest.mock.Mock(wraps=pub._set)
        assert not pub._update_task

        cancel_event = asyncio.Event()
        cancel_task = next(create_task(bg_cancel(cancel_event)))

        async def consume(pub: Publisher[str]):
            async for value in pub.subscribe(abort=cancel_event):
                if "9" in value:
                    break

        consume_task = next(create_task(consume(pub)))
        await asyncio.sleep(ONE_OP_TIME)

        # reset mock which was just called and check that bg processes are still running
        pub._set.reset_mock()
        assert not cancel_task.done()
        assert not consume_task.done()

        async for _ in pub.subscribe(abort=cancel_event):
            pub._set.assert_not_called()
            break

        # cleanup
        cancel_event.set()
        cancel_task.cancel()
        consume_task.cancel()

        await asyncio.sleep(0.01)
        assert cancel_task.done()
        assert consume_task.done()


class TestPublisher_Remove:
    async def test_should_cancel_update_task_if_no_subscribers(self):
        # create a data generator for the publisher
        x = 0

        async def get_next_value() -> str:
            nonlocal x
            x += 1
            return f"update {x}"

        pub = Publisher[str](maxsize=10, source=get_next_value, interval=ONE_OP_TIME)
        assert not pub._update_task

        # create subscription and let it run for a while
        sub = pub.add()
        iterations = 5
        await asyncio.sleep(ONE_OP_TIME * iterations)

        # check that internals are set and queue is being populated
        assert sub.qsize() >= iterations
        assert pub._update_task

        # save a reference to the task and remove the subscription
        task = pub._update_task
        pub.remove(sub)

        # check that internals from source are cleared
        assert not pub._update_task

        # give the task some to time to be gracefully cancelled
        await asyncio.sleep(0.01)
        assert task.cancelled()
