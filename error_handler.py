import time
import random
from functools import wraps


# -----------------------------------
# RETRY DECORATOR
# -----------------------------------

def retry_with_backoff(
    retries=3,
    base_delay=1
):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            for attempt in range(retries):

                try:

                    return func(*args, **kwargs)

                except Exception as e:

                    wait_time = (
                        base_delay * (2 ** attempt)
                    )

                    print(
                        f"\n[Retry {attempt + 1}]"
                    )

                    print(
                        f"Error: {e}"
                    )

                    print(
                        f"Waiting {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

            return {
                "error":
                f"{func.__name__} failed after retries."
            }

        return wrapper

    return decorator


# -----------------------------------
# FAILURE SIMULATION
# -----------------------------------

def random_failure(
    failure_rate=0.3
):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            if random.random() < failure_rate:

                raise Exception(
                    "Simulated API failure."
                )

            return func(*args, **kwargs)

        return wrapper

    return decorator