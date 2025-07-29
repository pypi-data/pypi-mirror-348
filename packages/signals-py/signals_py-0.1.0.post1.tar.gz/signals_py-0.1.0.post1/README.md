# signals
this project ports django's [signal dispatcher](https://docs.djangoproject.com/en/5.2/topics/signals/) so it can be used with any app


## Installation
```bash
pip install signals-py
```

(note that while it's installed as `signals-py`, the package name is `signals`)


## usage
for a full exploration check django's [docs](https://docs.djangoproject.com/en/5.2/topics/signals/)

but in essance:

### craete a signal:
```python
from signals.dispatch import Signal

my_costum_signal = Signal()
```

### define receviers
to connect a function/method as a recevier:
```python
from somewhere import my_costum_signal


def my_recevier(**kwargs):
    print("signal was sent!!")


my_costum_signal.connect(my_recevier)
```

or use the decorator
```python
from signals.dispatch import recevier
from somewhere import my_costum_signal


@recevier(my_costum_signal)
def my_recevier(**kwargs):
    print("signal was sent!!")

```

receviers can be async function/methods as well

```python
from somewhere import my_costum_signal


async def my_recevier(**kwargs):
    print("signal was sent!!")


my_costum_signal.connect(my_recevier)
```

or

```python
from signals.dispatch import recevier
from somewhere import my_costum_signal


@recevier(my_costum_signal)
async def my_recevier(**kwargs):
    print("signal was sent!!")

```


### send signals
to send a signal, simply call `.send()`:

```python
from somewhere import my_costum_signal

my_costum_signal.send(sender=object())
```

the sender argument is usually the class that's sending the signal (via `self.__class__`),
but it can be anything.

if one of the receviers raises an exception, it gets raise right there so other receviers won't be called.


or you can call `.send_robust()`, which ensures all receviers are called even if exceptions are raised
```python
from somewhere import my_costum_signal

my_costum_signal.send_robust(sender=object())
```

both `.send()` and `.send_robust()` have an async version, called `.asend()` and `.asend_robust()`

```python
from somewhere import my_costum_signal


async def do_some_work():
    await my_costum_signal.asend(sender=object)
    # or
    await my_costum_signal.asend_robust(sender=object)
```

all the sending methods return a list of tuples,
the first item in the tuple is the recevier, the second is the value returned by the recevier
if `send_robust` or `asend_robust` is used, if a recevier raises an exception, the exception will be the second item in the tuple.

### disconnect a recevier
to disconnect a recevier from a signal simply do:
```python
from somewhere import my_costum_signal
from receviers_home import my_recevier

my_costum_signal.disconnect(my_recevier)
```


## how async/sync receviers are treated
if you use `.send()` (or other sync ways to send), all sync receviers are called normally,
async receviers are wrappe in a single `asgiref.sync.async_to_sync` call.

if you use `.asend()` (or other async ways to send), async receviers are scheduled via `asyncio.gather()`
sync receviers are wrapped with a single `asgiref.sync.sync_to_async` then passed to the same `asyncio.gather()`

