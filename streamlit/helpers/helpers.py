import pandas as pd
import plotly.express as px
import streamlit as st


class KPI_Calculator:
    def __init__(self, df):
        self.df = df
        self.kpis = {}

    def calculate_pld_medio_diario(self):
        self.kpis["PLD Médio Diário"] = (
            self.df.groupby(["Data", "Submercado"])["Valor"].mean().reset_index()
        )

    def calculate_pld_medio_mensal(self):
        self.kpis["PLD Médio Mensal"] = (
            self.df.groupby([self.df["Data"].dt.to_period("M"), "Submercado"])["Valor"]
            .mean()
            .reset_index()
        )
        self.kpis["PLD Médio Mensal"]["Data"] = self.kpis["PLD Médio Mensal"][
            "Data"
        ].astype(str)

    def calculate_pld_maximo(self):
        self.kpis["PLD Máximo"] = (
            self.df.groupby(["Data", "Submercado"])["Valor"].max().reset_index()
        )

    def calculate_pld_minimo(self):
        self.kpis["PLD Mínimo"] = (
            self.df.groupby(["Data", "Submercado"])["Valor"].min().reset_index()
        )

    def calculate_desvio_padrao_diario(self):
        self.kpis["Desvio Padrão Diário"] = (
            self.df.groupby(["Data", "Submercado"])["Valor"].std().reset_index()
        )

    def calculate_spread_diario(self):
        self.kpis["Spread Diário"] = (
            self.kpis["PLD Máximo"]["Valor"] - self.kpis["PLD Mínimo"]["Valor"]
        ).reset_index(name="Valor")

    def calculate_pld_total_mensal(self):
        self.kpis["PLD Total Mensal"] = (
            self.df.groupby([self.df["Data"].dt.to_period("M"), "Submercado"])["Valor"]
            .sum()
            .reset_index()
        )
        self.kpis["PLD Total Mensal"]["Data"] = self.kpis["PLD Total Mensal"][
            "Data"
        ].astype(str)

    def calculate_numero_dias_acima_media(self):
        self.kpis["Número de Dias Acima da Média"] = (
            (self.df["Valor"] > self.df["Valor"].mean())
            .groupby([self.df["Data"], "Submercado"])
            .sum()
            .reset_index()
        )

    def calculate_kpis(self):
        st.info("Calculando KPIs...", icon="ℹ️")
        self.calculate_pld_medio_diario()
        self.calculate_pld_medio_mensal()
        self.calculate_pld_maximo()
        self.calculate_pld_minimo()
        self.calculate_desvio_padrao_diario()
        self.calculate_spread_diario()
        self.calculate_pld_total_mensal()
        self.calculate_numero_dias_acima_media()
        st.success("KPIs calculados com sucesso.", icon="✅")
        return self.kpis


# Função para visualização com Plotly
def plot_plotly(kpis, title, x, y):
    fig = px.line(kpis, x=x, y=y, color="Submercado", title=title)
    fig.update_layout(xaxis_title=x, yaxis_title=y)
    st.plotly_chart(fig)
    st.success(f"Gráfico {title} gerado com sucesso.", icon="✅")


# Função para visualização combinada com Plotly
def plot_combined_plotly(kpis, title, x, y_dict):
    fig = px.line()
    for y_label, y_data in y_dict.items():
        for submercado in kpis["Submercado"].unique():
            sub_df = kpis[kpis["Submercado"] == submercado]
            fig.add_scatter(
                x=sub_df[x],
                y=sub_df[y_data],
                mode="lines",
                name=f"{y_label} - {submercado}",
            )
    fig.update_layout(title=title, xaxis_title=x, yaxis_title="Valor")
    st.plotly_chart(fig)
    st.success(f"Gráfico {title} gerado com sucesso.", icon="✅")
