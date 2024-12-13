import streamlit as st
from helpers.helpers import calculate_desvio_padrao_diario, calculate_spread_diario
import plotly.graph_objects as go


def plot_desvio_padrao_spread_diario(df):
    kpis_std = calculate_desvio_padrao_diario(df)
    kpis_spread = calculate_spread_diario(df)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=kpis_std["Data"],
            y=kpis_std["Valor"],
            mode="lines",
            name="Desvio Padrão Diário",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=kpis_spread["Data"],
            y=kpis_spread["Valor"],
            mode="lines",
            name="Spread Diário",
        )
    )
    fig.update_layout(
        title="Desvio Padrão e Spread Diário", xaxis_title="Data", yaxis_title="Valor"
    )
    st.plotly_chart(fig)


def desvio_padrao_spread_diario_tab(df):
    st.header("Desvio Padrão e Spread Diário")
    st.write(
        "**Desvio Padrão Diário**: Mede a variabilidade dos preços diários em relação à média, indicando a volatilidade do mercado em um determinado período."
        "\n\n**Spread Diário**: Representa a diferença entre o PLD máximo e mínimo de cada dia, evidenciando a amplitude das variações de preço."
    )
    plot_desvio_padrao_spread_diario(df)
