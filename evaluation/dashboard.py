"""
Evaluation dashboard — runs all 22 quality metrics against benchmark outputs.
"""

from pathlib import Path
from evaluation.metrics import score_report


# ---------------------------------------------------------------------------
# Load benchmark files
# ---------------------------------------------------------------------------

benchmark_dir = Path("evaluation/benchmarks")
benchmarks: dict[str, str] = {}
for file in benchmark_dir.glob("*.md"):
    benchmarks[file.stem] = file.read_text()


# ---------------------------------------------------------------------------
# Sample generated outputs (replace with real agent outputs in production)
# ---------------------------------------------------------------------------

generated_outputs = {
    "microsoft": """
    ## Executive Summary
    Microsoft Corporation (NASDAQ: MSFT) is a multinational technology company headquartered
    in Redmond, Washington. In Q1 FY2024, revenue grew 13% year-over-year to $56.5B.
    Azure cloud revenue increased 28% YoY. The company faces regulatory risks in the EU
    regarding its $69B Activision acquisition. However, competitive advantages remain
    strong across enterprise software, cloud, and AI. Revenue growth is expected to
    continue through 2025 and 2026 as AI integration deepens across Microsoft 365.

    ## Financial Analysis
    Microsoft reported total revenue of $211.9B in FY2023, a 7% increase from FY2022.
    Intelligent Cloud segment revenue reached $87.9B, up 19% YoY, driven by Azure
    growth of 28%. Operating income rose 6% to $88.5B. The company maintains an
    operating margin of approximately 42%, reflecting strong pricing power and
    scalable infrastructure. According to the 10-K filing, gross margin improved
    to 69.4% in FY2023.

    ## Risk Assessment
    Key financial risks include macroeconomic slowdown, competitive pressure from
    AWS and Google Cloud, and regulatory scrutiny. Operational risks include
    cybersecurity threats and reliance on third-party hardware. However, Microsoft's
    diversified revenue base and recurring subscription model provide resilience.

    ## Competitive Positioning
    Azure holds approximately 22% cloud market share, behind AWS at 32%. Despite this,
    Azure's growth rate of 28% outpaces AWS's 13% in recent quarters. Microsoft's
    integration with Office 365 and Teams provides competitive moats in enterprise
    accounts. The Copilot AI strategy positions Microsoft well for 2025-2027 outlook.

    ## Outlook
    Revenue forecasts for FY2025 point to continued double-digit growth, with Azure
    projected to maintain 25-30% growth rates. Management guidance (Reuters, Bloomberg)
    suggests confidence in AI monetization. Cross-source synthesis of SEC filings and
    earnings calls confirms this trajectory, consistent with strong enterprise demand.
    """,

    "apple": """
    ## Executive Summary
    Apple Inc. (NASDAQ: AAPL) reported record revenue of $383.3B in FY2023.
    Despite a 3% YoY revenue decline, gross margins expanded to 44.1%.
    The Services segment grew 16% YoY to $85.2B, offsetting hardware weakness.
    Regulatory risk includes EU Digital Markets Act compliance costs. However,
    Apple's ecosystem competitive advantage remains a significant moat.

    ## Financial Analysis
    Apple's iPhone revenue declined 2% YoY to $200.6B in FY2023, while Mac
    revenue fell 27% to $29.4B due to PC market weakness. Gross margin of 44.1%
    represents a five-year high (10-K filing, SEC EDGAR). Services operating
    margin exceeds 70%, driving overall profitability. EPS grew 3% to $6.13.

    ## Risk Assessment
    Financial risks include declining consumer hardware demand and macroeconomic
    headwinds in China (40% of supply chain). Regulatory risks from EU and DOJ
    antitrust investigations. Competitive risks from Samsung, Xiaomi, and Google.
    Despite these, Apple's installed base of 2B devices provides revenue resilience.

    ## Competitive Positioning
    Apple controls 18% of global smartphone market share. The walled-garden
    ecosystem generates 94% customer retention. In contrast, Android competitors
    struggle with fragmented software updates. Revenue diversification into
    Services, Wearables, and Apple TV+ reduces hardware concentration risk.

    ## Outlook
    Management expects Services to reach $100B by 2025 (Bloomberg analyst consensus).
    Vision Pro spatial computing launch targets enterprise and creative markets.
    However, headwinds in China remain a risk factor for FY2025 forecasts.
    """,

    "tesla": """
    ## Executive Summary
    Tesla Inc. (NASDAQ: TSLA) delivered 1.81M vehicles in FY2023, a 38% YoY increase.
    Revenue grew 19% to $96.8B, while net income fell 53% to $15B due to price cuts.
    Automotive gross margin declined from 29% to 18%, reflecting competitive pricing
    pressure. However, Energy Generation and Storage revenue grew 54% YoY.

    ## Financial Analysis
    Tesla's automotive revenue reached $82.4B in FY2023, up 15% YoY. Despite volume
    growth, average selling prices fell ~15% due to aggressive price reductions
    (10-K, SEC EDGAR). Energy segment revenue of $6B grew 54%, becoming a significant
    growth driver. Free cash flow of $4.4B declined 51% YoY. Operating margin of
    8.2% versus 17.2% in FY2022 signals margin compression.

    ## Risk Assessment
    Key risks include competitive pressure from BYD and legacy automakers, regulatory
    uncertainty around EV tax credits, macroeconomic sensitivity, and CEO concentration
    risk. Operational risks include Gigafactory production ramp challenges.
    Financial risks include rising capital expenditure requirements for next-gen platform.

    ## Competitive Positioning
    Tesla holds approximately 18% of global EV market share, down from 24% in 2022
    as BYD surpassed Tesla in deliveries in Q4 2023. However, Tesla's Supercharger
    network of 50,000+ stations and FSD software stack provide competitive advantages
    consistent with strong long-term positioning. Despite competitive headwinds,
    brand loyalty remains high according to earnings call transcript analysis.

    ## Outlook
    Management guidance projects 20-30% delivery growth in 2025 and 2026.
    Cybertruck ramp and next-generation $25K vehicle are catalysts. Scenario
    analysis suggests EPS recovery to $5-7 range by 2026 if margins stabilize.
    Reuters and Bloomberg forecasts align with this trajectory.
    """,
}


# ---------------------------------------------------------------------------
# Run evaluation pipeline
# ---------------------------------------------------------------------------

results: dict[str, dict] = {}

for company, generated in generated_outputs.items():
    benchmark = benchmarks.get(company, "")
    results[company] = score_report(
        generated=generated,
        benchmark=benchmark,
        tool_calls=6,
        successful_calls=6,
        total_errors=1,
        recovered_errors=1,
        memory_hits=2,
        total_api_calls=6,
        elapsed_seconds=90.0,
    )


# ---------------------------------------------------------------------------
# Print dashboard
# ---------------------------------------------------------------------------

def print_dashboard(results: dict) -> None:
    width = 60
    print("\n" + "=" * width)
    print("EVALUATION DASHBOARD  —  22-Metric Framework")
    print("=" * width)

    category_headers = {
        "FA": "FACTUAL ACCURACY",
        "CO": "COMPLETENESS",
        "AD": "ANALYTICAL DEPTH",
        "CS": "COHERENCE & STRUCTURE",
        "AB": "AGENT BEHAVIOUR",
    }

    for company, metrics in results.items():
        print(f"\n{'─' * width}")
        print(f"  {company.upper()}")
        print(f"{'─' * width}")

        current_category = None
        for metric_key, value in metrics.items():
            category = metric_key.split("-")[0]
            if category != current_category:
                current_category = category
                print(f"\n  [{category_headers.get(category, category)}]")

            label = metric_key.split("_", 1)[1].replace("_", " ").title()
            bar_len = int(value * 20)
            bar = "█" * bar_len + "░" * (20 - bar_len)
            print(f"    {metric_key[:6]:8s} {label:35s} {bar}  {value:.2f}")

        avg = sum(metrics.values()) / len(metrics)
        print(f"\n  {'Overall Average':45s} {avg:.2f}")

    print("\n" + "=" * width + "\n")


if __name__ == "__main__":
    print_dashboard(results)
