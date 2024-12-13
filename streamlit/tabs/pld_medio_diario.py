import streamlit as st
import plotly.express as px
import pandas as pd
from helpers.helpers import apply_filters


def calculate_pld_medio_diario(df):
    return (
        df.groupby(["Data", "Submercado"], as_index=False)["Valor"].mean().reset_index()
    )


def plot_pld_medio_diario(df):
    kpis = calculate_pld_medio_diario(df)
    fig = px.line(
        kpis, x="Data", y="Valor", color="Submercado", title="PLD Médio Diário"
    )
    st.plotly_chart(fig)


def pld_medio_diario_tab(df):
    st.header("PLD Médio Diário")
    st.write(
        "Representa a média diária dos preços de liquidação das diferenças (PLD) calculados para cada dia. "
        "Essa métrica ajuda a identificar tendências diárias e flutuações no custo da energia elétrica."
    )
    df_filtered = apply_filters(
        df,
        date_key="date_filter_medio_diario",
        submercado_key="submercado_filter_medio_diario",
    )
    plot_pld_medio_diario(df_filtered)
