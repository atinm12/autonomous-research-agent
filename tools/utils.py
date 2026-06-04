import time
from functools import wraps


# -------------------------
# SIMPLE IN-MEMORY CACHE
# -------------------------

cache = {}


def cache_result(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        # Include function name so different tools with the same input don't collide
        key = func.__name__ + str(args) + str(kwargs)

        if key in cache:
            print("\nUsing cached result...")
            return cache[key]

        result = func(*args, **kwargs)
        cache[key] = result
        return result

    return wrapper


# -------------------------
# RATE LIMITING DECORATOR
# -------------------------

def rate_limit(seconds=2):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            print(f"\nRate limiting: sleeping for {seconds} seconds...")

            time.sleep(seconds)

            return func(*args, **kwargs)

        return wrapper

    return decorator