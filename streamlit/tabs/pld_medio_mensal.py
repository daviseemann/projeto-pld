import streamlit as st
import plotly.express as px
import pandas as pd
from helpers.helpers import apply_filters


def calculate_pld_medio_mensal(df):
    result = (
        df.groupby([df["Data"].dt.to_period("M"), "Submercado"])["Valor"]
        .mean()
        .reset_index()
    )
    result["Data"] = result["Data"].astype(str)
    return result


def plot_pld_medio_mensal(df):
    kpis = calculate_pld_medio_mensal(df)
    fig = px.line(
        kpis, x="Data", y="Valor", color="Submercado", title="PLD Médio Mensal"
    )
    st.plotly_chart(fig)


def pld_medio_mensal_tab(df):
    st.header("PLD Médio Mensal")
    st.write(
        "Mostra a média dos valores diários do PLD agregados por mês. "
        "É útil para análise de tendências de longo prazo e sazonalidades no mercado de energia."
    )
    df_filtered = apply_filters(
        df,
        date_key="date_filter_medio_mensal",
        submercado_key="submercado_filter_medio_mensal",
    )
    plot_pld_medio_mensal(df_filtered)
