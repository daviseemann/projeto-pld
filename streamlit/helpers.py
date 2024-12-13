import pandas as pd
import plotly.express as px
import streamlit as st


# Funções para cálculo de KPIs
def calculate_kpis(df):
    st.info("Calculando KPIs...", icon="ℹ️")
    kpis = {}
    # Calcular PLD Médio Diário
    kpis["PLD Médio Diário"] = df.groupby("Data")["Valor"].mean().reset_index()
    # Calcular PLD Médio Mensal
    kpis["PLD Médio Mensal"] = (
        df.groupby(df["Data"].dt.to_period("M"))["Valor"].mean().reset_index()
    )
    kpis["PLD Médio Mensal"]["Data"] = kpis["PLD Médio Mensal"]["Data"].astype(str)
    # Calcular PLD Máximo
    kpis["PLD Máximo"] = df.groupby("Data")["Valor"].max().reset_index()
    # Calcular PLD Mínimo
    kpis["PLD Mínimo"] = df.groupby("Data")["Valor"].min().reset_index()
    # Calcular Desvio Padrão Diário
    kpis["Desvio Padrão Diário"] = df.groupby("Data")["Valor"].std().reset_index()
    # Calcular Spread Diário
    kpis["Spread Diário"] = (
        kpis["PLD Máximo"]["Valor"] - kpis["PLD Mínimo"]["Valor"]
    ).reset_index(name="Valor")
    # Calcular PLD Total Mensal
    kpis["PLD Total Mensal"] = (
        df.groupby(df["Data"].dt.to_period("M"))["Valor"].sum().reset_index()
    )
    kpis["PLD Total Mensal"]["Data"] = kpis["PLD Total Mensal"]["Data"].astype(str)
    # Calcular Número de Dias Acima da Média
    kpis["Número de Dias Acima da Média"] = (
        (df["Valor"] > df["Valor"].mean()).groupby(df["Data"]).sum().reset_index()
    )
    st.success("KPIs calculados com sucesso.", icon="✅")
    return kpis


# Função para visualização com Plotly
def plot_plotly(kpis, title, x, y):
    fig = px.line(kpis, x=x, y=y, title=title)
    fig.update_layout(xaxis_title=x, yaxis_title=y)
    st.plotly_chart(fig)
    st.success(f"Gráfico {title} gerado com sucesso.", icon="✅")


# Função para visualização combinada com Plotly
def plot_combined_plotly(kpis, title, x, y_dict):
    fig = px.line(title=title)
    for y_label, y_data in y_dict.items():
        fig.add_scatter(x=kpis[x], y=kpis[y_data], mode="lines", name=y_label)
    fig.update_layout(xaxis_title=x, yaxis_title="Valor")
    st.plotly_chart(fig)
    st.success(f"Gráfico {title} gerado com sucesso.", icon="✅")
