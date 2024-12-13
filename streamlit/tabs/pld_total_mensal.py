import streamlit as st
import plotly.express as px
import pandas as pd
from helpers.helpers import apply_filters


def calculate_pld_total_mensal(df):
    result = (
        df.groupby([df["Data"].dt.to_period("M"), "Submercado"])["Valor"]
        .sum()
        .reset_index()
    )
    result["Data"] = result["Data"].astype(str)
    return result


def plot_pld_total_mensal(df):
    kpis = calculate_pld_total_mensal(df)
    fig = px.line(
        kpis, x="Data", y="Valor", color="Submercado", title="PLD Total Mensal"
    )
    st.plotly_chart(fig)


def pld_total_mensal_tab(df):
    st.header("PLD Total Mensal")
    st.write(
        "Soma dos valores diários do PLD em um mês. "
        "Essa métrica reflete o impacto agregado do custo da energia ao longo de um período mensal."
    )
    df_filtered = apply_filters(
        df,
        date_key="date_filter_total_mensal",
        submercado_key="submercado_filter_total_mensal",
    )
    plot_pld_total_mensal(df_filtered)
