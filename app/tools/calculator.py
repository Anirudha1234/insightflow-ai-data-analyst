def calculate_profit(revenue: float, cost: float) -> float:

    return round(revenue - cost, 2)


def calculate_profit_margin(revenue: float, cost: float) -> float:

    if revenue == 0:
        raise ValueError("Revenue cannot be zero.")

    profit = revenue - cost

    return round((profit / revenue) * 100, 2)


def calculate_average_order_value(revenue: float, total_orders: int) -> float:

    if total_orders <= 0:
        raise ValueError("Total orders must be greater than zero.")

    return round(revenue / total_orders, 2)


def calculate_growth(current_value: float, previous_value: float) -> float:

    if previous_value == 0:
        raise ValueError("Previous value cannot be zero.")

    growth = ((current_value - previous_value) / previous_value) * 100

    return round(growth, 2)


def calculate_percentage(part: float, total: float) -> float:

    if total == 0:
        raise ValueError("Total cannot be zero.")

    return round((part / total) * 100, 2)
