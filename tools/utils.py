import time
from functools import wraps


# -------------------------
# SIMPLE IN-MEMORY CACHE
# -------------------------

cache = {}


def cache_result(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        # Create unique cache key
        key = str(args) + str(kwargs)

        # Check if result already exists
        if key in cache:

            print("\nUsing cached result...")

            return cache[key]

        # Run actual function
        result = func(*args, **kwargs)

        # Save result
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