def handle_error_node(state: dict) -> dict:

    error = state.get("error")

    return {
        "status": "error",
        "answer": (
            "I could not complete your analysis because an error occurred.\n\n"
            f"Error details: {error}\n\n"
            "Please check your question or try again."
        ),
    }


def handle_no_data_node(state: dict) -> dict:

    return {
        "status": "no_data",
        "answer": (
            "Your query executed successfully, but no matching records "
            "were found.\n\n"
            "Try changing the date range or adjusting your question."
        ),
    }
