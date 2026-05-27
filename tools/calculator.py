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