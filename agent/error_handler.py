"""
Error handling utilities — retry with exponential backoff + jitter,
random failure injection for testing.
"""

import time
import random
from functools import wraps


# -------------------------------------------------------------------
# RETRY WITH EXPONENTIAL BACKOFF AND JITTER
# Spec: initial delay 1s, doubles each attempt, up to 5 retries.
# Jitter: random 0–500ms to prevent thundering-herd problems.
# -------------------------------------------------------------------

def retry_with_backoff(retries: int = 5, base_delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == retries - 1:
                        # Final attempt failed — return error dict
                        return {"error": f"{func.__name__} failed after {retries} retries: {e}"}

                    jitter = random.uniform(0, 0.5)
                    wait_time = base_delay * (2 ** attempt) + jitter

                    print(f"\n[Retry {attempt + 1}/{retries}] {func.__name__} failed: {e}")
                    print(f"  Waiting {wait_time:.1f}s before retry...")
                    time.sleep(wait_time)

        return wrapper
    return decorator


# -------------------------------------------------------------------
# RANDOM FAILURE INJECTION (for testing / Challenge 8 simulation)
# -------------------------------------------------------------------

def random_failure(failure_rate: float = 0.3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if random.random() < failure_rate:
                raise Exception(
                    f"Simulated {int(failure_rate * 100)}% failure in {func.__name__}."
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator
