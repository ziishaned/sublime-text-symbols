from functools import partial, wraps
from timeit import default_timer

import sublime


def debounce(delay_in_ms, sync=False):
    """Delay calls to functions until they weren't triggered for n ms."""

    # We assume that locking is not necessary because each function will be called
    # from either the ui or the async thread only.
    set_timeout = sublime.set_timeout if sync else sublime.set_timeout_async

    def decorator(func):
        call_at = 0

        def _debounced_callback(callback):
            nonlocal call_at
            diff = call_at - int(default_timer() * 1000)
            if diff > 0:
                set_timeout(partial(_debounced_callback, callback), diff)
            else:
                call_at = 0
                callback()

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal call_at
            pending = call_at > 0
            call_at = int(default_timer() * 1000) + delay_in_ms
            if pending:
                return
            callback = partial(func, *args, **kwargs)
            set_timeout(partial(_debounced_callback, callback), delay_in_ms)

        return wrapper

    return decorator
