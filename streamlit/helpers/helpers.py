import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime, timedelta


def calculate_pld_maximo(df):
    return df.groupby(["Data", "Submercado"])["Valor"].max().reset_index()


def calculate_pld_minimo(df):
    return df.groupby(["Data", "Submercado"])["Valor"].min().reset_index()


def calculate_desvio_padrao_diario(df):
    return df.groupby(["Data", "Submercado"])["Valor"].std().reset_index()


def calculate_spread_diario(df):
    pld_maximo = calculate_pld_maximo(df)
    pld_minimo = calculate_pld_minimo(df)
    spread_diario = pld_maximo.copy()
    spread_diario["Valor"] = pld_maximo["Valor"] - pld_minimo["Valor"]
    return spread_diario


def apply_filters(df, date_key="date_filter", submercado_key="submercado_filter"):
    st.header("Filtros")
    col1, col2 = st.columns(2)

    # Definir intervalo de datas padrão como o ano corrente, de 01/01 até o momento no ano
    end_date = df["Data"].max().date()
    start_date = datetime(end_date.year, 1, 1).date()

    with col1:
        data_filter = st.date_input(
            "Selecione o intervalo de datas:",
            [start_date, end_date],
            min_value=df["Data"].min().date(),
            max_value=end_date,
            key=date_key,
        )
    data_filter = pd.to_datetime(data_filter)

    with col2:
        if "Submercado" in df.columns:
            submercado_filter = st.segmented_control(
                "Selecione os submercados:",
                options=df["Submercado"].unique(),
                default=df["Submercado"].unique(),
                selection_mode="multi",
                key=submercado_key,
            )

            df_filtered = df[
                (df["Data"] >= data_filter[0])
                & (df["Data"] <= data_filter[1])
                & (df["Submercado"].isin(submercado_filter))
            ]
        else:
            st.warning("A coluna 'Submercado' não está presente nos dados.")
            df_filtered = df[
                (df["Data"] >= data_filter[0]) & (df["Data"] <= data_filter[1])
            ]

    return df_filtered
