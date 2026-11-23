import plotly.express as px
import pandas as pd


def generate_bar_chart(df: pd.DataFrame, x: str, y: str, title: str):
    fig = px.bar(df, x=x, y=y, title=title, text_auto=".2s")

    fig.update_layout(
        template="plotly_white",
        xaxis_title=x.replace("_", " ").title(),
        yaxis_title=y.replace("_", " ").title(),
    )

    return fig


def generate_line_chart(df: pd.DataFrame, x: str, y: str, title: str):
    fig = px.line(df, x=x, y=y, title=title, markers=True)

    fig.update_layout(
        template="plotly_white",
        xaxis_title=x.replace("_", " ").title(),
        yaxis_title=y.replace("_", " ").title(),
    )

    return fig


def generate_pie_chart(df: pd.DataFrame, names: str, values: str, title: str):
    fig = px.pie(df, names=names, values=values, title=title, hole=0.35)

    fig.update_layout(template="plotly_white")

    return fig


def generate_scatter_chart(df: pd.DataFrame, x: str, y: str, title: str):
    fig = px.scatter(df, x=x, y=y, title=title)

    fig.update_layout(
        template="plotly_white",
        xaxis_title=x.replace("_", " ").title(),
        yaxis_title=y.replace("_", " ").title(),
    )

    return fig
