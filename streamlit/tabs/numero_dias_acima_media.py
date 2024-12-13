import streamlit as st
import plotly.express as px
import pandas as pd
from helpers.helpers import apply_filters


def calculate_numero_dias_acima_media(df):
    media_valor = df["Valor"].mean()
    result = (
        df.groupby(["Data", "Submercado"])
        .apply(lambda x: (x["Valor"] > media_valor).sum())
        .reset_index()
    )
    result.columns = ["Data", "Submercado", "Valor"]
    return result


def plot_numero_dias_acima_media(df):
    kpis = calculate_numero_dias_acima_media(df)
    fig = px.line(
        kpis,
        x="Data",
        y="Valor",
        color="Submercado",
        title="Número de Dias Acima da Média",
    )
    st.plotly_chart(fig)


def numero_dias_acima_media_tab(df):
    st.header("Número de Dias Acima da Média")
    st.write(
        "Quantifica o número de dias em que os valores diários do PLD excederam a média geral. "
        "Essa métrica identifica períodos mais caros e pode ser usada para destacar anomalias ou padrões de alta demanda."
    )
    df_filtered = apply_filters(
        df,
        date_key="date_filter_acima_media",
        submercado_key="submercado_filter_acima_media",
    )
    plot_numero_dias_acima_media(df_filtered)
