from app.agents.graph import analyst_graph

# question = """
# Show the top 5 products by revenue
# from delivered orders in 2025.
# """

# question = """
# Show revenue by product category in 2025
# and visualize it using a bar chart.
# """

# question = """
# Show the total revenue by product category in 2025.
# """

# question = """
# Show revenue by product category in 2025
# and visualize it using a bar chart.
# """

# question = """
# Show revenue by product category in 2025
# and visualize it using a pie chart.
# """

# question = """
# Show monthly revenue for delivered orders in 2025
# and visualize it using a line chart.
# """

# question = """
# For each product, show its average selling price
# and total revenue from delivered orders in 2025.
# Visualize the relationship using a scatter chart.
# """

# question = """
# Calculate the average order value for delivered orders in 2025
# """

# question = "Calculate revenue growth in delivered orders from 2024 to 2025"

# question = "Calculate the percentage contribution of Electronics category to total delivered revenue in 2025"

question = "Plot monthly delivered revenue for 2025"


result = analyst_graph.invoke(
    {
        "question": question,
        "sql_query": None,
        "dataframe": None,
        "analysis": None,
        "chart_path": None,
        "chart_required": None,
        "chart_type": None,
        "answer": None,
        "error": None,
        "status": None,
    }
)


print("\n--- GENERATED SQL ---")
print(result["sql_query"])


print("\n--- QUERY RESULTS ---")
print(result["dataframe"])


print("\n--- DATA ANALYSIS ---")
print(result["analysis"])


print("\n--- FINAL BUSINESS ANSWER ---")
print(result["answer"])


print("\n--- STATUS ---")
print(result["status"])

print("\n--- FINAL ANSWER ---")
print(result["answer"])

print("\n--- CHART INFORMATION ---")
print("Chart required:", result["chart_required"])
print("Chart type:", result["chart_type"])
print("Chart path:", result["chart_path"])

print("\n--- PYTHON ANALYSIS ---")
print(result.get("python_analysis"))

print("\n--- CALCULATOR RESULTS ---")
print(result.get("calculations"))

# Test case for handling invalid SQL

# from app.tools.sql_executor import execute_sql

# print("\n--- INVALID SQL TEST ---")

# try:
#     execute_sql("SELECT * FROM unauthorized_table")
# except Exception as error:
#     print("Error handled successfully:")
#     print(error)


# Test case for handling errors in the workflow

# import app.agents.nodes as agent_nodes

# print("\n--- LANGGRAPH ERROR ROUTING TEST ---")

# # Temporarily replace Gemini SQL generation
# original_generate_sql = agent_nodes.generate_sql

# agent_nodes.generate_sql = lambda question: ("SELECT * FROM unauthorized_table")

# try:
#     error_result = analyst_graph.invoke(
#         {
#             "question": "Test error handling",
#             "sql_query": None,
#             "dataframe": None,
#             "analysis": None,
#             "chart_path": None,
#             "answer": None,
#             "error": None,
#             "status": None,
#         }
#     )

#     print("Status:", error_result["status"])
#     print("Answer:", error_result["answer"])

# finally:
#     # Restore the original function
#     agent_nodes.generate_sql = original_generate_sql


# Test case for handling empty query results

# import pandas as pd

# import app.agents.nodes as agent_nodes

# print("\n--- EMPTY RESULT TEST ---")

# original_generate_sql = agent_nodes.generate_sql
# original_execute_sql = agent_nodes.execute_sql

# # Return valid SQL
# agent_nodes.generate_sql = lambda question: (
#     "SELECT * FROM products WHERE product_id = -999"
# )

# # Simulate a successful query with zero rows
# agent_nodes.execute_sql = lambda sql: pd.DataFrame(
#     columns=["product_id", "product_name"]
# )

# try:
#     empty_result = analyst_graph.invoke(
#         {
#             "question": "Find a product that does not exist",
#             "sql_query": None,
#             "dataframe": None,
#             "analysis": None,
#             "chart_path": None,
#             "answer": None,
#             "error": None,
#             "status": None,
#         }
#     )

#     print("Status:", empty_result["status"])
#     print("Answer:", empty_result["answer"])

# finally:
#     agent_nodes.generate_sql = original_generate_sql
#     agent_nodes.execute_sql = original_execute_sql


# Simulate Gemini answer-generation failure

# import app.agents.nodes as agent_nodes

# print("\n--- GEMINI ANSWER FAILURE TEST ---")

# original_generate_response = agent_nodes.generate_response


# # Simulate Gemini API failure
# def mock_generate_response(prompt):
#     raise RuntimeError("Simulated Gemini API failure")


# agent_nodes.generate_response = mock_generate_response

# try:
#     failure_result = analyst_graph.invoke(
#         {
#             "question": "Show top 5 products by revenue in 2025",
#             "sql_query": None,
#             "dataframe": None,
#             "analysis": None,
#             "chart_path": None,
#             "answer": None,
#             "error": None,
#             "status": None,
#         }
#     )

#     print("Status:", failure_result["status"])
#     print("Answer:", failure_result["answer"])

# finally:
#     # Restore the original Gemini function
#     agent_nodes.generate_response = original_generate_response


# PostgreSQL execution error

# import app.agents.nodes as agent_nodes

# print("\n--- POSTGRESQL EXECUTION FAILURE TEST ---")

# original_generate_sql = agent_nodes.generate_sql

# # Valid SQL syntax, but nonexistent database column
# agent_nodes.generate_sql = lambda question: ("SELECT nonexistent_column FROM products")

# try:
#     db_error_result = analyst_graph.invoke(
#         {
#             "question": "Test PostgreSQL execution failure",
#             "sql_query": None,
#             "dataframe": None,
#             "analysis": None,
#             "chart_path": None,
#             "answer": None,
#             "error": None,
#             "status": None,
#         }
#     )

#     print("Status:", db_error_result["status"])
#     print("Answer:", db_error_result["answer"])

# finally:
#     agent_nodes.generate_sql = original_generate_sql
