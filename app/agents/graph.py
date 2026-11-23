from langgraph.graph import StateGraph, START, END

from app.agents.state import AnalystState

from app.agents.nodes import (
    generate_sql_node,
    execute_sql_node,
    analyze_data_node,
    generate_answer_node,
)

from app.agents.error_handler import handle_error_node, handle_no_data_node

from app.agents.chart_nodes import check_chart_requirement_node, generate_chart_node

from app.agents.analysis_nodes import python_analysis_node

from app.agents.calculator_nodes import calculator_node


def check_status(state: dict) -> str:

    if state.get("status") == "error":
        return "error"

    return "continue"


def check_results(state: dict) -> str:

    if state["dataframe"].empty:
        return "no_data"

    return "continue"


workflow = StateGraph(AnalystState)

workflow.add_node("generate_sql", generate_sql_node)
workflow.add_node("execute_sql", execute_sql_node)
workflow.add_node("analyze_data", analyze_data_node)
workflow.add_node("generate_answer", generate_answer_node)
workflow.add_node("check_chart_requirement", check_chart_requirement_node)
workflow.add_node("generate_chart", generate_chart_node)
workflow.add_node("python_analysis", python_analysis_node)
workflow.add_node("calculator", calculator_node)

workflow.add_node("handle_error", handle_error_node)
workflow.add_node("handle_no_data", handle_no_data_node)


workflow.add_edge(START, "generate_sql")

workflow.add_conditional_edges(
    "generate_sql", check_status, {"continue": "execute_sql", "error": "handle_error"}
)

workflow.add_conditional_edges(
    "execute_sql", check_status, {"continue": "check_results", "error": "handle_error"}
)

workflow.add_node("check_results", lambda state: {})

workflow.add_conditional_edges(
    "check_results",
    check_results,
    {"continue": "analyze_data", "no_data": "handle_no_data"},
)

workflow.add_conditional_edges(
    "analyze_data",
    check_status,
    {"continue": "python_analysis", "error": "handle_error"},
)

workflow.add_conditional_edges(
    "python_analysis", check_status, {"continue": "calculator", "error": "handle_error"}
)

workflow.add_conditional_edges(
    "calculator", check_status, {"continue": "generate_answer", "error": "handle_error"}
)

workflow.add_conditional_edges(
    "generate_answer",
    check_status,
    {"continue": "check_chart_requirement", "error": "handle_error"},
)

workflow.add_conditional_edges(
    "check_chart_requirement",
    lambda state: ("generate_chart" if state["chart_required"] else "end"),
    {"generate_chart": "generate_chart", "end": END},
)

workflow.add_conditional_edges(
    "generate_chart", check_status, {"continue": END, "error": "handle_error"}
)

workflow.add_edge("handle_error", END)
workflow.add_edge("handle_no_data", END)

analyst_graph = workflow.compile()
