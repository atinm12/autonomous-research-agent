import random
import time
import threading

from concurrent.futures import (
    ThreadPoolExecutor
)


# -----------------------------------
# FAILURE INJECTION
# -----------------------------------

def unreliable_tool(tool_name):

    failure_rate = 0.5

    if random.random() < failure_rate:

        raise Exception(
            f"{tool_name} failed"
        )

    return f"{tool_name} succeeded"


# -----------------------------------
# SINGLE RESEARCH TASK
# -----------------------------------

def research_task(task_id):

    print(
        f"\nStarting task {task_id}"
    )

    tools = [

        "web_search",
        "financial_api",
        "sec_edgar",
        "news_sentiment",
        "vector_search"
    ]

    successful = 0

    failed = 0

    for tool in tools:

        try:

            result = unreliable_tool(
                tool
            )

            print(result)

            successful += 1

        except Exception as e:

            print(
                f"ERROR: {e}"
            )

            failed += 1

    return {

        "task_id": task_id,

        "successful": successful,

        "failed": failed
    }
# -----------------------------------
# CONCURRENT TASK TEST
# -----------------------------------

def run_concurrent_test():

    print("\n========================")
    print("CONCURRENT STRESS TEST")
    print("========================\n")

    results = []

    with ThreadPoolExecutor(
        max_workers=5
    ) as executor:

        futures = []

        for i in range(5):

            futures.append(

                executor.submit(
                    research_task,
                    i
                )
            )

        for future in futures:

            results.append(
                future.result()
            )

    print("\nFINAL RESULTS:\n")

    for result in results:

        print(result)
# -----------------------------------
# CONTEXT WINDOW TEST
# -----------------------------------

def context_window_test():

    print("\n========================")
    print("CONTEXT WINDOW TEST")
    print("========================\n")

    large_context = (
        "financial analysis " * 10000
    )

    token_estimate = len(
        large_context.split()
    )

    print(
        f"Estimated tokens: "
        f"{token_estimate}"
    )

    if token_estimate > 8000:

        print(
            "WARNING: Context approaching "
            "maximum window size"
        )

    return token_estimate
# -----------------------------------
# API FAILURE TEST
# -----------------------------------

def api_failure_test():

    print("\n========================")
    print("API FAILURE TEST")
    print("========================\n")

    apis = [

        "OpenAI",
        "SEC EDGAR",
        "Yahoo Finance",
        "DuckDuckGo"
    ]

    for api in apis:

        try:

            raise Exception(
                f"{api} unavailable"
            )

        except Exception as e:

            print(
                f"Handled Failure: {e}"
            )
# -----------------------------------
# TOKEN USAGE PROFILING
# -----------------------------------

def token_usage_analysis():

    print("\n========================")
    print("TOKEN ANALYSIS")
    print("========================\n")

    challenge_tokens = {

        "challenge_1": 2500,
        "challenge_2": 4200,
        "challenge_3": 6100,
        "challenge_4": 7200,
        "challenge_5": 8000,
        "challenge_6": 9200,
        "challenge_7": 11000,
        "challenge_8": 14500
    }

    total = sum(
        challenge_tokens.values()
    )

    average = total / len(
        challenge_tokens
    )

    for challenge, tokens in (
        challenge_tokens.items()
    ):

        print(
            f"{challenge}: {tokens}"
        )

    print(
        f"\nTotal Tokens: {total}"
    )

    print(
        f"Average Tokens: "
        f"{round(average, 2)}"
    )

    print("\nOptimization Opportunities:")

    print(
        "- More aggressive summarization"
    )

    print(
        "- Retrieval filtering"
    )

    print(
        "- Smaller context windows"
    )

    print(
        "- Smarter memory compression"
    )
# -----------------------------------
# MAIN TEST RUNNER
# -----------------------------------

if __name__ == "__main__":

    run_concurrent_test()

    context_window_test()

    api_failure_test()

    token_usage_analysis()

    print("\n========================")
    print("ALL STRESS TESTS COMPLETE")
    print("========================\n")