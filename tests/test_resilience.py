from agent.error_handler import (
    retry_with_backoff,
    random_failure
)

from agent.fallback_chains import (
    execute_with_fallbacks
)

from agent.circuit_breaker import (
    CircuitBreaker
)


print("\n========================")
print("RESILIENCE TEST")
print("========================\n")


# -----------------------------------
# RETRY TEST
# -----------------------------------

@retry_with_backoff(
    retries=3,
    base_delay=1
)

@random_failure(
    failure_rate=0.7
)

def unstable_api():

    return "API succeeded."


print("\n--- RETRY TEST ---\n")

print(
    unstable_api()
)


# -----------------------------------
# FALLBACK TEST
# -----------------------------------

print("\n--- FALLBACK TEST ---\n")

fallback_result = (
    execute_with_fallbacks(
        "company_profile",
        "MSFT"
    )
)

print(fallback_result)


# -----------------------------------
# CIRCUIT BREAKER TEST
# -----------------------------------

breaker = CircuitBreaker(
    failure_threshold=2,
    recovery_timeout=5
)


def failing_tool():

    raise Exception(
        "Tool failure."
    )


print("\n--- CIRCUIT BREAKER TEST ---\n")

print(
    breaker.call(failing_tool)
)

print(
    breaker.call(failing_tool)
)

print(
    breaker.call(failing_tool)
)


print("\n========================")
print("ALL RESILIENCE TESTS COMPLETE")
print("========================\n")