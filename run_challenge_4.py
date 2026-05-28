from agent.core import ResearchAgent


query = """
Produce a comprehensive 4000-5000 word comparative analysis of the three
major public cloud platforms: Amazon Web Services (AWS), Microsoft Azure,
and Google Cloud Platform (GCP).

Use the available tools to gather real financial data, then write a
structured long-form report covering ALL of the following areas in depth:

1. Revenue figures and year-over-year growth rates for each platform
   (use financial_data_api with tickers AMZN, MSFT, GOOGL and
    sec_filing_search to pull segment-level data)

2. Market share estimates and how share has shifted over the past 3 years
   (use peer_comparison with input "AWS,Azure,GCP" and web_search)

3. Operating margins and profitability trends per division
   (use calculation_engine to compute growth rates and margins from
    the raw figures returned by financial_data_api)

4. Competitive advantages and strategic differentiation for each platform
   (use earnings_transcript for AMZN, MSFT, GOOGL and web_search)

5. Risks, headwinds, and forward outlook

The final report must be 4000-5000 words, written in full prose paragraphs,
with specific numbers cited throughout. Do not write a short summary.
Each section must hit its word target — do not truncate any section early.
"""


agent = ResearchAgent()

result = agent.run(query)

print("\n" + "=" * 80)
print("CHALLENGE 4 RESULT")
print("=" * 80)
print(result)