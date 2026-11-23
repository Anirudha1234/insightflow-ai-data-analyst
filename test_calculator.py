from app.tools.calculator import (
    calculate_profit,
    calculate_profit_margin,
    calculate_average_order_value,
    calculate_growth,
    calculate_percentage,
)

# Profit
profit = calculate_profit(revenue=100000, cost=70000)

print("Profit:", profit)


# Profit margin
margin = calculate_profit_margin(revenue=100000, cost=70000)

print("Profit Margin:", margin, "%")


# Average Order Value
aov = calculate_average_order_value(revenue=500000, total_orders=100)

print("Average Order Value:", aov)


# Growth
growth = calculate_growth(current_value=414479117.54, previous_value=290033761.06)

print("Revenue Growth:", growth, "%")


# Percentage contribution
contribution = calculate_percentage(part=291498157.06, total=414479117.54)

print("Electronics Contribution:", contribution, "%")
