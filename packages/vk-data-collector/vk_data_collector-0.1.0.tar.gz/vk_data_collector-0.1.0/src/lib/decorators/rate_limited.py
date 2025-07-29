import time
from collections import deque
from functools import wraps


def rate_limited(limit: int):
    requests: deque[float] = deque(maxlen=limit)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()

            if len(requests) == limit:
                earliest = requests[0]
                if now - earliest < 1:
                    sleep_time = 1 - (now - earliest)
                    time.sleep(max(0, sleep_time))

            requests.append(now)
            return func(*args, **kwargs)

        return wrapper

    return decorator
