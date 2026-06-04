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

    Accepts:
      - A {"data": [...]} array of company dicts with revenue/margin fields
        (the most common LLM call pattern for multi-company analysis)
      - A plain-English string: 'growth 411 321', 'margin 125 411', 'dcf ...'

    Supported calculation types (detected from keywords):
      - data array:   {"data": [{"ticker":..,"revenue":..,"operating_margin":..}]}
      - growth rate:  'growth <current> <previous>'
      - margin:       'margin <net_income> <revenue>'
      - dcf:          'dcf <cash_flow> <growth_rate> <discount_rate>'
      - market share: 'market share <segment> <total>'
    """
    import re
    import json

    raw = str(input_str).strip()

    # ---------------------------------------------------------------
    # Handle {"data": [...]} multi-company array (most common LLM call)
    # ---------------------------------------------------------------
    try:
        parsed = json.loads(raw)
        data = parsed.get("data") if isinstance(parsed, dict) else None
        if data and isinstance(data, list):
            results = []
            for item in data:
                ticker  = item.get("ticker", "Unknown")
                revenue = item.get("revenue", 0) or 0
                op_mg   = item.get("operating_margin")
                rev_gr  = item.get("revenue_growth")
                grs_mg  = item.get("gross_margin")
                net_mg  = item.get("profit_margin")
                ebitda  = item.get("ebitda", 0) or 0
                entry = {"ticker": ticker}
                if revenue:
                    entry["revenue_billions"] = round(revenue / 1e9, 2)
                if op_mg is not None:
                    entry["operating_margin_pct"] = round(op_mg * 100, 2)
                if rev_gr is not None:
                    entry["revenue_growth_pct"]   = round(rev_gr * 100, 2)
                if grs_mg is not None:
                    entry["gross_margin_pct"]     = round(grs_mg * 100, 2)
                if net_mg is not None:
                    entry["net_margin_pct"]       = round(net_mg * 100, 2)
                if ebitda and revenue:
                    entry["ebitda_margin_pct"]    = round(ebitda / revenue * 100, 2)
                results.append(entry)
            return {
                "calculation_type": "multi_company_metrics",
                "results": results,
                "interpretation": (
                    "Converted raw financial figures to percentage metrics "
                    "for direct comparison across companies."
                )
            }
    except (json.JSONDecodeError, ValueError, TypeError):
        pass

    text    = raw.lower()
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