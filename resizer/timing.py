import functools
import time


RECORDED_TIMES = {}


def get_total_run_time_for(name):
    return RECORDED_TIMES.get(name, 0)


def record_run_time_for(name):
    def monitor_decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            start = time.time()
            r = f(*args, **kwargs)
            RECORDED_TIMES[name] = time.time() - start
            return r
        return wrapped
    return monitor_decorator
