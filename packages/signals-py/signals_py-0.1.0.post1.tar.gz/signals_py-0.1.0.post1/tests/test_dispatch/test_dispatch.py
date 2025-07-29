import asyncio
import logging
import re
import weakref
from types import TracebackType

import pytest

from signals.dispatch import Signal, receiver
from signals.dispatch.dispatcher import _make_id
from signals.test.utils import garbage_collect

from lazy_settings.test.utils import override_settings

pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"


def receiver_1_arg(val, **kwargs):
    return val


async def receiver_1_arg_async(val, **kwargs):
    return val


class Callable:
    def __call__(self, val, **kwargs):
        return val

    def a(self, val, **kwargs):
        return val


a_signal = Signal()
b_signal = Signal()
c_signal = Signal()
d_signal = Signal(use_caching=True)


class TestDispatcher:
    def assert_test_is_clean(self, signal: Signal):
        assert not signal.has_listeners()
        assert signal.receivers == []

    @override_settings(DEBUG=True)
    def test_cannot_connect_no_kwargs(self):
        def receiver_no_kwargs(sender):
            pass

        msg = re.escape("Signal receivers must accept keyword arguments (**kwargs).")
        with pytest.raises(ValueError, match=msg):
            a_signal.connect(receiver_no_kwargs)
        self.assert_test_is_clean(a_signal)

    @override_settings(DEBUG=True)
    def test_cannot_connect_non_callable(self):
        msg = "Signal receivers must be callable."
        with pytest.raises(TypeError, match=msg):
            a_signal.connect(object())
        self.assert_test_is_clean(a_signal)

    def test_send(self):
        a_signal.connect(receiver_1_arg, sender=self)
        a_signal.connect(receiver_1_arg_async, sender=self)
        result = a_signal.send(sender=self, val="test")
        assert result == [(receiver_1_arg, "test"), (receiver_1_arg_async, "test")]
        a_signal.disconnect(receiver_1_arg, sender=self)
        a_signal.disconnect(receiver_1_arg_async, sender=self)
        self.assert_test_is_clean(a_signal)

    def test_send_no_receivers(self):
        result = a_signal.send(sender=self, val="test")
        assert result == []

    def test_send_connected_no_sender(self):
        a_signal.connect(receiver_1_arg)
        a_signal.connect(receiver_1_arg_async)
        result = a_signal.send(sender=self, val="test")
        assert result == [(receiver_1_arg, "test"), (receiver_1_arg_async, "test")]
        a_signal.disconnect(receiver_1_arg)
        a_signal.disconnect(receiver_1_arg_async)
        self.assert_test_is_clean(a_signal)

    def test_send_different_no_sender(self):
        a_signal.connect(receiver_1_arg, sender=object)
        a_signal.connect(receiver_1_arg_async, object)
        result = a_signal.send(sender=self, val="test")
        assert result == []
        a_signal.disconnect(receiver_1_arg, sender=object)
        a_signal.disconnect(receiver_1_arg_async, sender=object)
        self.assert_test_is_clean(a_signal)

    def test_unweakrefable_sender(self):
        sender = object()
        a_signal.connect(receiver_1_arg, sender=sender)
        a_signal.connect(receiver_1_arg_async, sender=sender)
        result = a_signal.send(sender=sender, val="test")
        assert result == [(receiver_1_arg, "test"), (receiver_1_arg_async, "test")]
        a_signal.disconnect(receiver_1_arg, sender=sender)
        a_signal.disconnect(receiver_1_arg_async, sender=sender)
        self.assert_test_is_clean(a_signal)

    def test_garbage_collected_receiver(self):
        a = Callable()
        a_signal.connect(a.a, sender=self)
        del a
        garbage_collect()
        result = a_signal.send(sender=self, val="test")
        assert result == []
        self.assert_test_is_clean(a_signal)

    def test_garbage_collected_sender(self, mocker):
        signal = Signal()

        class Sender:
            pass

        def make_id(target):
            """
            Simulate id() reuse for distinct senders with non-overlapping
            lifetimes that would require memory contention to reproduce.
            """
            if isinstance(target, Sender):
                return 0
            return _make_id(target)

        def first_receiver(attempt, **kwargs):
            return attempt

        async def first_async_receiver(attempt, **kwargs):
            return attempt

        def second_receiver(attempt, **kwargs):
            return attempt

        async def second_async_receiver(attempt, **kwargs):
            return attempt

        mocker.patch("signals.dispatch.dispatcher._make_id", make_id)
        sender = Sender()
        signal.connect(first_receiver, sender)
        signal.connect(first_async_receiver, sender)
        result = signal.send(sender, attempt="first")
        assert result == [(first_receiver, "first"), (first_async_receiver, "first")]

        del sender
        garbage_collect()

        sender = Sender()
        signal.connect(second_receiver, sender)
        signal.connect(second_async_receiver, sender)
        result = signal.send(sender, attempt="second")
        assert result == [
            (second_receiver, "second"),
            (second_async_receiver, "second"),
        ]

    def test_cached_garbaged_collected(self):
        """
        Make sure signal caching sender receivers don't prevent garbage
        collection of senders.
        """

        class sender:
            pass

        wref = weakref.ref(sender)
        d_signal.connect(receiver_1_arg)
        d_signal.connect(receiver_1_arg_async)
        d_signal.send(sender, val="garbage")
        del sender
        garbage_collect()
        try:
            assert wref() is None
        finally:
            # Disconnect after reference check since it flushes the tested cache.
            d_signal.disconnect(receiver_1_arg)
            d_signal.disconnect(receiver_1_arg_async)

    def test_multiple_registration(self):
        a = Callable()
        a_signal.connect(a)
        a_signal.connect(a)
        a_signal.connect(a)
        a_signal.connect(a)
        a_signal.connect(a)
        a_signal.connect(a)

        result = a_signal.send(sender=self, val="test")
        assert len(result) == 1
        assert len(a_signal.receivers) == 1
        del a
        del result
        garbage_collect()
        self.assert_test_is_clean(a_signal)

    def test_uid_registration(self):
        def uid_based_receiver_1(**kwargs):
            pass

        async def uid_based_receiver_1_async(**kwargs):
            pass

        def uid_based_receiver_2(**kwargs):
            pass

        async def uid_based_receiver_2_async(**kwargs):
            pass

        a_signal.connect(uid_based_receiver_1, dispatch_uid="uid")
        a_signal.connect(uid_based_receiver_1_async, dispatch_uid="uid")
        a_signal.connect(uid_based_receiver_2, dispatch_uid="uid")
        a_signal.connect(uid_based_receiver_2_async, dispatch_uid="uid")
        assert len(a_signal.receivers) == 1
        a_signal.disconnect(dispatch_uid="uid")
        self.assert_test_is_clean(a_signal)

    def test_send_robust_success(self):
        a_signal.connect(receiver_1_arg)
        a_signal.connect(receiver_1_arg_async)
        result = a_signal.send_robust(sender=self, val="test")
        assert result == [(receiver_1_arg, "test"), (receiver_1_arg_async, "test")]
        a_signal.disconnect(receiver_1_arg)
        a_signal.disconnect(receiver_1_arg_async)
        self.assert_test_is_clean(a_signal)

    def test_send_robust_no_receivers(self):
        result = a_signal.send_robust(sender=self, val="test")
        assert result == []

    def test_send_robust_ignored_sender(self):
        a_signal.connect(receiver_1_arg)
        a_signal.connect(receiver_1_arg_async)
        result = a_signal.send_robust(sender=self, val="test")
        assert result == [(receiver_1_arg, "test"), (receiver_1_arg_async, "test")]
        a_signal.disconnect(receiver_1_arg)
        a_signal.disconnect(receiver_1_arg_async)
        self.assert_test_is_clean(a_signal)

    def test_send_robust_fail(self, caplog):
        def fails(val, **kwargs):
            raise ValueError("this")

        a_signal.connect(fails)
        try:
            with caplog.at_level(logging.ERROR, logger="signals.dispatch"):
                result = a_signal.send_robust(sender=self, val="test")
            err = result[0][1]
            assert isinstance(err, ValueError)
            assert err.args == ("this",)
            assert hasattr(err, "__traceback__")
            assert isinstance(err.__traceback__, TracebackType)

            log_record = caplog.records[0]
            assert (
                log_record.getMessage() == "Error calling "
                "TestDispatcher.test_send_robust_fail.<locals>.fails in "
                "Signal.send_robust() (this)"
            )
            assert log_record.exc_info
            _, exc_value, _ = log_record.exc_info
            assert isinstance(exc_value, ValueError)
            assert str(exc_value) == "this"
        finally:
            a_signal.disconnect(fails)

        self.assert_test_is_clean(a_signal)

    def test_disconnection(self):
        receiver_1 = Callable()
        receiver_2 = Callable()
        receiver_3 = Callable()

        a_signal.connect(receiver_1)
        a_signal.connect(receiver_2)
        a_signal.connect(receiver_3)

        a_signal.disconnect(receiver_1)
        del receiver_2
        garbage_collect()
        a_signal.disconnect(receiver_3)
        self.assert_test_is_clean(a_signal)

    def test_values_returned_by_disconnection(self):
        receiver_1 = Callable()
        receiver_2 = Callable()

        a_signal.connect(receiver_1)
        receiver_1_disconnected = a_signal.disconnect(receiver_1)
        receiver_2_disconnected = a_signal.disconnect(receiver_2)
        assert receiver_1_disconnected
        assert receiver_2_disconnected is False
        self.assert_test_is_clean(a_signal)

    def test_has_listeners(self):
        assert a_signal.has_listeners() is False
        assert a_signal.has_listeners() is False
        receiver_1 = Callable()
        a_signal.connect(receiver_1)
        assert a_signal.has_listeners()
        assert a_signal.has_listeners(sender=object())
        a_signal.disconnect(receiver_1)
        assert a_signal.has_listeners() is False
        assert a_signal.has_listeners(sender=object()) is False


class TestDispatcherAsync:
    def assert_test_is_clean(self, signal: Signal):
        assert not signal.has_listeners()
        assert signal.receivers == []

    async def test_asend(self):
        a_signal.connect(receiver_1_arg_async, sender=self)
        result = await a_signal.asend(sender=self, val="test")
        assert result == [(receiver_1_arg_async, "test")]
        a_signal.disconnect(receiver_1_arg_async, sender=self)
        self.assert_test_is_clean(a_signal)

    async def test_asend_no_receivers(self):
        result = await a_signal.asend(sender=self, val="test")
        assert result == []

    async def test_asend_connected_no_sender(self):
        a_signal.connect(receiver_1_arg_async)
        result = await a_signal.asend(sender=self, val="test")
        assert result == [(receiver_1_arg_async, "test")]
        a_signal.disconnect(receiver_1_arg_async)
        self.assert_test_is_clean(a_signal)

    async def test_asend_different_no_sender(self):
        a_signal.connect(receiver_1_arg_async, sender=object)
        result = await a_signal.asend(sender=self, val="test")
        assert result == []
        a_signal.disconnect(receiver_1_arg_async, sender=object)
        self.assert_test_is_clean(a_signal)

    async def test_unweakrefable_sender(self):
        sender = object()
        a_signal.connect(receiver_1_arg_async, sender=sender)
        result = await a_signal.asend(sender=sender, val="test")
        assert result == [(receiver_1_arg_async, "test")]
        a_signal.disconnect(receiver_1_arg_async, sender=sender)
        self.assert_test_is_clean(a_signal)

    async def test_garbage_collected_receiver(self):
        a = Callable()
        a_signal.connect(a.a, sender=self)
        del a
        garbage_collect()
        result = await a_signal.asend(sender=self, val="test")
        assert result == []
        self.assert_test_is_clean(a_signal)

    async def test_garbage_collected_sender(self, mocker):
        signal = Signal()

        class Sender:
            pass

        def make_id(target):
            """
            Simulate id() reuse for distinct senders with non-overlapping
            lifetimes that would require memory contention to reproduce.
            """
            if isinstance(target, Sender):
                return 0
            return _make_id(target)

        async def first_receiver(attempt, **kwargs):
            return attempt

        async def second_receiver(attempt, **kwargs):
            return attempt

        mocker.patch("signals.dispatch.dispatcher._make_id", make_id)
        sender = Sender()
        signal.connect(first_receiver, sender)
        result = await signal.asend(sender, attempt="first")
        assert result == [(first_receiver, "first")]

        del sender
        garbage_collect()

        sender = Sender()
        signal.connect(second_receiver, sender)
        result = await signal.asend(sender, attempt="second")
        assert result == [(second_receiver, "second")]

    async def test_cached_garbaged_collected(self):
        """
        Make sure signal caching sender receivers don't prevent garbage
        collection of senders.
        """

        class sender:
            pass

        wref = weakref.ref(sender)
        d_signal.connect(receiver_1_arg_async)
        await d_signal.asend(sender, val="garbage")
        del sender
        garbage_collect()
        try:
            assert wref() is None
        finally:
            # Disconnect after reference check since it flushes the tested cache.
            d_signal.disconnect(receiver_1_arg_async)

    async def test_multiple_registration(self):
        a = Callable()
        a_signal.connect(a)
        a_signal.connect(a)
        a_signal.connect(a)
        a_signal.connect(a)
        a_signal.connect(a)
        a_signal.connect(a)
        result = await a_signal.asend(sender=self, val="test")
        assert len(result) == 1
        assert len(a_signal.receivers) == 1
        del a
        del result
        garbage_collect()
        await asyncio.sleep(0)
        self.assert_test_is_clean(a_signal)

    async def test_send_robust_success(self):
        a_signal.connect(receiver_1_arg_async)
        result = await a_signal.asend_robust(sender=self, val="test")
        assert result == [(receiver_1_arg_async, "test")]
        a_signal.disconnect(receiver_1_arg_async)
        self.assert_test_is_clean(a_signal)

    async def test_send_robust_no_receivers(self):
        result = await a_signal.asend_robust(sender=self, val="test")
        assert result == []

    async def test_send_robust_ignored_sender(self):
        a_signal.connect(receiver_1_arg_async)
        result = await a_signal.asend_robust(sender=self, val="test")
        assert result == [(receiver_1_arg_async, "test")]
        a_signal.disconnect(receiver_1_arg_async)
        self.assert_test_is_clean(a_signal)

    async def test_send_robust_fail(self, caplog):
        def fails(val, **kwargs):
            raise ValueError("this")

        a_signal.connect(fails)
        try:
            with caplog.at_level(logging.ERROR, logger="signals.dispatch"):
                result = await a_signal.asend_robust(sender=self, val="test")
            err = result[0][1]
            assert isinstance(err, ValueError)
            assert err.args == ("this",)
            assert hasattr(err, "__traceback__")
            assert isinstance(err.__traceback__, TracebackType)

            log_record = caplog.records[0]
            assert (
                log_record.getMessage() == "Error calling "
                "TestDispatcherAsync.test_send_robust_fail.<locals>.fails in "
                "Signal.send_robust() (this)"
            )
            assert log_record.exc_info
            _, exc_value, _ = log_record.exc_info
            assert isinstance(exc_value, ValueError)
            assert str(exc_value) == "this"
        finally:
            a_signal.disconnect(fails)

        self.assert_test_is_clean(a_signal)


class TestReceiver:
    def test_receiver_single_signal(self):
        @receiver(a_signal)
        def f(val, **kwargs):
            self.state = val

        self.state = False
        a_signal.send(sender=self, val=True)
        assert self.state is True

    async def test_async_receiver_single_signal(self):
        @receiver(a_signal)
        async def f(val, **kwargs):
            self.state = val

        self.state = False
        await a_signal.asend(sender=self, val=True)
        assert self.state is True

    def test_receiver_signal_list(self):
        @receiver([a_signal, b_signal, c_signal])
        def f(val, **kwargs):
            self.state.append(val)

        self.state = []
        a_signal.send(sender=self, val="a")
        c_signal.send(sender=self, val="c")
        b_signal.send(sender=self, val="b")
        assert "a" in self.state
        assert "b" in self.state
        assert "c" in self.state

    async def test_async_receiver_signal_list(self):
        @receiver([a_signal, b_signal, c_signal])
        async def f(val, **kwargs):
            self.state.append(val)

        self.state = []
        await a_signal.asend(sender=self, val="a")
        await c_signal.asend(sender=self, val="c")
        await b_signal.asend(sender=self, val="b")
        assert "a" in self.state
        assert "b" in self.state
        assert "c" in self.state
