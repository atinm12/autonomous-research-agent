from evaluation.metrics import *

from pathlib import Path


# -----------------------------------
# LOAD BENCHMARKS
# -----------------------------------

benchmark_dir = Path(
    "evaluation/benchmarks"
)

benchmarks = {}

for file in benchmark_dir.glob("*.md"):

    benchmarks[file.stem] = (
        file.read_text()
    )


# -----------------------------------
# SAMPLE GENERATED OUTPUTS
# -----------------------------------

generated_outputs = {

    "microsoft":
    """
    Microsoft is a technology company
    focused on cloud computing,
    AI, enterprise software,
    and gaming strategy.
    """,

    "apple":
    """
    Apple operates a major
    hardware and services ecosystem
    with strong profitability.
    """,

    "tesla":
    """
    Tesla develops electric vehicles,
    AI systems, and energy products.
    """
}


# -----------------------------------
# EVALUATION PIPELINE
# -----------------------------------

results = {}

for company, generated in (
    generated_outputs.items()
):

    benchmark = benchmarks.get(
        company,
        ""
    )

    results[company] = {

        "numerical_accuracy":
        numerical_accuracy_score(
            generated,
            benchmark
        ),

        "citation_score":
        citation_score(
            generated
        ),

        "hallucination_score":
        hallucination_score(
            generated,
            benchmark
        ),

        "insight_density":
        insight_density_score(
            generated
        ),

        "logical_flow":
        logical_flow_score(
            generated
        ),

        "executive_summary":
        executive_summary_score(
            generated
        ),

        "tool_efficiency":
        tool_efficiency_score(
            10,
            9
        )
    }


# -----------------------------------
# PRINT DASHBOARD
# -----------------------------------

print("\n========================")
print("EVALUATION DASHBOARD")
print("========================\n")

for company, metrics in (
    results.items()
):

    print(f"\n--- {company.upper()} ---\n")

    for metric, value in (
        metrics.items()
    ):

        print(
            f"{metric}: {value}"
        )