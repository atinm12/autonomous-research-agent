def calculate_growth_rate(current, previous):

    if previous == 0:
        return "Cannot divide by zero."

    growth = ((current - previous) / previous) * 100

    return round(growth, 2)


def calculate_profit_margin(net_income, revenue):

    if revenue == 0:
        return "Cannot divide by zero."

    margin = (net_income / revenue) * 100

    return round(margin, 2)


def simple_dcf(cash_flow, growth_rate, discount_rate, years=5):

    total_value = 0

    for year in range(1, years + 1):

        future_cash_flow = cash_flow * ((1 + growth_rate) ** year)

        discounted = future_cash_flow / ((1 + discount_rate) ** year)

        total_value += discounted

    return round(total_value, 2)


def calculation_engine(input_str):
    """
    Dispatch function for the agent's calculation_engine tool.

    Accepts a plain-English string describing the calculation,
    parses out numbers where possible, and returns a structured result.

    Supported calculation types (detected from keywords):
      - growth rate:  'growth <current> <previous>'
      - margin:       'margin <net_income> <revenue>'
      - dcf:          'dcf <cash_flow> <growth_rate> <discount_rate>'
    """
    import re

    text = str(input_str).lower().strip()
    numbers = [float(n) for n in re.findall(r"[-+]?\d*\.?\d+", text)]

    if "growth" in text:
        if len(numbers) >= 2:
            result = calculate_growth_rate(numbers[0], numbers[1])
            return {
                "calculation_type": "revenue_growth_rate",
                "current": numbers[0],
                "previous": numbers[1],
                "result_percent": result,
                "interpretation": f"Year-over-year growth of {result}%"
            }
        return {"error": "growth rate requires two numbers: current and previous"}

    elif "margin" in text:
        if len(numbers) >= 2:
            result = calculate_profit_margin(numbers[0], numbers[1])
            return {
                "calculation_type": "profit_margin",
                "net_income": numbers[0],
                "revenue": numbers[1],
                "result_percent": result,
                "interpretation": f"Operating/profit margin of {result}%"
            }
        return {"error": "margin calculation requires two numbers: net_income and revenue"}

    elif "dcf" in text or "discounted" in text:
        if len(numbers) >= 3:
            result = simple_dcf(numbers[0], numbers[1], numbers[2])
            return {
                "calculation_type": "dcf_valuation",
                "cash_flow": numbers[0],
                "growth_rate": numbers[1],
                "discount_rate": numbers[2],
                "result_value": result,
                "interpretation": f"5-year DCF present value: {result}"
            }
        return {"error": "DCF requires three numbers: cash_flow, growth_rate, discount_rate"}

    elif "market share" in text or "share" in text:
        if len(numbers) >= 2:
            share = round((numbers[0] / numbers[1]) * 100, 2)
            return {
                "calculation_type": "market_share",
                "segment": numbers[0],
                "total": numbers[1],
                "result_percent": share,
                "interpretation": f"Market share of {share}%"
            }
        return {"error": "market share requires two numbers: segment and total"}

    else:
        return {
            "error": "Unrecognised calculation type. Use keywords: growth, margin, dcf, market share.",
            "hint": "Example: 'growth rate 411 321' or 'margin 125 411'"
        }