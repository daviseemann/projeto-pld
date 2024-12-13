import streamlit as st
import pandas as pd
from helpers.helpers import (
    KPI_Calculator,
    plot_plotly,
    plot_combined_plotly,
)  # Importar funções auxiliares

from helpers.data_pipeline import download_pld, clean_pld_data

# Configuração da página
st.set_page_config(
    page_title="Painel de preços de liquidação diária",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Função para carregar os dados
@st.cache_data
def load_data():
    st.info("Carregando os dados...", icon="ℹ️")
    df = pd.read_csv("data/clean_data.csv")
    st.success("Dados carregados com sucesso!", icon="✅")
    df["Data"] = pd.to_datetime(df["Data"])
    return df


# Botão para recarregar os dados
if st.sidebar.button("Recarregar dados"):
    download_pld()
    clean_pld_data()
    st.cache_data.clear()


# Carregar os dados
df_reshaped = load_data()

# Adicionar filtros
st.sidebar.header("Filtros")
data_filter = st.sidebar.date_input(
    "Selecione o intervalo de datas:",
    [df_reshaped["Data"].min().date(), df_reshaped["Data"].max().date()],
    min_value=df_reshaped["Data"].min().date(),
    max_value=df_reshaped["Data"].max().date(),
)
data_filter = pd.to_datetime(data_filter)

submercado_filter = st.sidebar.multiselect(
    "Selecione os submercados:",
    options=df_reshaped["Submercado"].unique(),
    default=df_reshaped["Submercado"].unique(),
)

# Aplicar filtros
df_filtered = df_reshaped[
    (df_reshaped["Data"] >= data_filter[0])
    & (df_reshaped["Data"] <= data_filter[1])
    & (df_reshaped["Submercado"].isin(submercado_filter))
]

# Calcular KPIs com os dados filtrados
kpi_calculator = KPI_Calculator(df_filtered)
kpis = kpi_calculator.calculate_kpis()

# Navegação de páginas
page = st.sidebar.selectbox(
    "Selecione a página",
    [
        "PLD Médio Diário",
        "PLD Médio Mensal",
        "PLD Máximo e Mínimo",
        "Desvio Padrão e Spread Diário",
        "PLD Total Mensal",
        "Número de Dias Acima da Média",
    ],
)

# Aplicação Streamlit
st.title("Dashboard de KPIs do PLD")

# Visualizar gráficos com base na página selecionada
if page == "PLD Médio Diário":
    st.header("PLD Médio Diário")
    st.write(
        "Representa a média diária dos preços de liquidação das diferenças (PLD) calculados para cada dia. "
        "Essa métrica ajuda a identificar tendências diárias e flutuações no custo da energia elétrica."
    )
    plot_plotly(kpis["PLD Médio Diário"], "PLD Médio Diário", "Data", "Valor")
elif page == "PLD Médio Mensal":
    st.header("PLD Médio Mensal")
    st.write(
        "Mostra a média dos valores diários do PLD agregados por mês. "
        "É útil para análise de tendências de longo prazo e sazonalidades no mercado de energia."
    )
    plot_plotly(kpis["PLD Médio Mensal"], "PLD Médio Mensal", "Data", "Valor")
elif page == "PLD Máximo e Mínimo":
    st.header("PLD Máximo e Mínimo")
    st.write(
        "Apresenta os valores máximos e mínimos do PLD registrados diariamente. "
        "Esses extremos fornecem insights sobre os períodos de maior e menor estresse no mercado de energia."
    )
    plot_combined_plotly(
        kpis,
        "PLD Máximo e Mínimo",
        "Data",
        {"PLD Máximo": "PLD Máximo", "PLD Mínimo": "PLD Mínimo"},
    )
elif page == "Desvio Padrão e Spread Diário":
    st.header("Desvio Padrão e Spread Diário")
    st.write(
        "**Desvio Padrão Diário**: Mede a variabilidade dos preços diários em relação à média, indicando a volatilidade do mercado em um determinado período."
        "\n\n**Spread Diário**: Representa a diferença entre o PLD máximo e mínimo de cada dia, evidenciando a amplitude das variações de preço."
    )
    plot_combined_plotly(
        kpis,
        "Desvio Padrão e Spread Diário",
        "Data",
        {
            "Desvio Padrão Diário": "Desvio Padrão Diário",
            "Spread Diário": "Spread Diário",
        },
    )
elif page == "PLD Total Mensal":
    st.header("PLD Total Mensal")
    st.write(
        "Soma dos valores diários do PLD em um mês. "
        "Essa métrica reflete o impacto agregado do custo da energia ao longo de um período mensal."
    )
    plot_plotly(kpis["PLD Total Mensal"], "PLD Total Mensal", "Data", "Valor")
elif page == "Número de Dias Acima da Média":
    st.header("Número de Dias Acima da Média")
    st.write(
        "Quantifica o número de dias em que os valores diários do PLD excederam a média geral. "
        "Essa métrica identifica períodos mais caros e pode ser usada para destacar anomalias ou padrões de alta demanda."
    )
    plot_plotly(
        kpis["Número de Dias Acima da Média"],
        "Número de Dias Acima da Média",
        "Data",
        "Valor",
    )
