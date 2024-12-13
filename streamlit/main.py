import streamlit as st
import pandas as pd
import time
from helpers.data_pipeline import (
    download_pld,
    clean_pld_data,
    get_latest_clean_data_file,
)
from tabs.pld_medio_diario import pld_medio_diario_tab
from tabs.pld_medio_mensal import pld_medio_mensal_tab
from tabs.pld_maximo_minimo import pld_maximo_minimo_tab
from tabs.desvio_padrao_spread_diario import desvio_padrao_spread_diario_tab
from tabs.pld_total_mensal import pld_total_mensal_tab
from tabs.numero_dias_acima_media import numero_dias_acima_media_tab
from tabs.arquitetura_da_plataforma import arquitetura_da_plataforma

# Configuração da página
st.set_page_config(
    page_title="Painel de preços de liquidação diária",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.logo("./images/compass_energy_logo.svg", size="large")


# Função para carregar os dados
@st.cache_data
def load_data():
    with st.sidebar.status("Carregando os dados...", expanded=True) as status:
        st.spinner("Carregando os dados...")
        latest_file = get_latest_clean_data_file()
        df = pd.read_csv(latest_file)
        status.update(
            label="Dados carregados com sucesso!", state="complete", expanded=False
        )
        df["Data"] = pd.to_datetime(df["Data"])
        return df


with st.sidebar.status("Downloading data...", expanded=True) as status:
    st.spinner("Downloading data...")
    download_pld()
    st.spinner("Limpando os dados...")
    clean_pld_data()
    st.spinner("Dados limpos carregando graficos...")
    st.cache_data.clear()
    status.update(label="Download complete!", state="complete", expanded=False)

# Botão para recarregar os dados
st.sidebar.button("Recarregar dados")

# Carregar os dados
df_reshaped = load_data()

# Navegação de páginas
tabs = st.tabs(
    [
        "PLD Médio Diário",
        "PLD Médio Mensal",
        "PLD Máximo e Mínimo",
        "Desvio Padrão e Spread Diário",
        "PLD Total Mensal",
        "Número de Dias Acima da Média",
        "Arquitetura da plataforma",
    ],
)

# Visualizar gráficos com base na página selecionada
with tabs[0]:
    pld_medio_diario_tab(df_reshaped)

with tabs[1]:
    pld_medio_mensal_tab(df_reshaped)

with tabs[2]:
    pld_maximo_minimo_tab(df_reshaped)

with tabs[3]:
    desvio_padrao_spread_diario_tab(df_reshaped)

with tabs[4]:
    pld_total_mensal_tab(df_reshaped)

with tabs[5]:
    numero_dias_acima_media_tab(df_reshaped)

with tabs[6]:
    arquitetura_da_plataforma()

# Rodapé
st.sidebar.markdown(
    """
---
**Autores:** Davi Seemann e Pedro Paladini  
**Instituição:** Universidade Federal de Santa Catarina
"""
)
st.sidebar.image("./images/brasao_UFSC_vertical_extenso.svg", width=100)
