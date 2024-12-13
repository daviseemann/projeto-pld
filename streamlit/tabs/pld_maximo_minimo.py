import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from helpers.helpers import apply_filters


def calculate_pld_maximo(df):
    return df.groupby(["Data", "Submercado"])["Valor"].max().reset_index()


def calculate_pld_minimo(df):
    return df.groupby(["Data", "Submercado"])["Valor"].min().reset_index()


def plot_pld_maximo_minimo(df):
    kpis_max = calculate_pld_maximo(df)
    kpis_min = calculate_pld_minimo(df)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=kpis_max["Data"], y=kpis_max["Valor"], mode="lines", name="PLD Máximo"
        )
    )
    fig.add_trace(
        go.Scatter(
            x=kpis_min["Data"], y=kpis_min["Valor"], mode="lines", name="PLD Mínimo"
        )
    )
    fig.update_layout(
        title="PLD Máximo e Mínimo", xaxis_title="Data", yaxis_title="Valor"
    )
    st.plotly_chart(fig)


def pld_maximo_minimo_tab(df):
    st.header("PLD Máximo e Mínimo")
    st.write(
        "Apresenta os valores máximos e mínimos do PLD registrados diariamente. "
        "Esses extremos fornecem insights sobre os períodos de maior e menor estresse no mercado de energia."
    )
    df_filtered = apply_filters(
        df,
        date_key="date_filter_maximo_minimo",
        submercado_key="submercado_filter_maximo_minimo",
    )
    plot_pld_maximo_minimo(df_filtered)
