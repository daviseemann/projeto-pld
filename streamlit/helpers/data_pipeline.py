import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import os
import streamlit as st


def download_pld():
    # URL do site
    url = "https://www.ccee.org.br/web/guest/precos/painel-precos"

    # Fazer a requisição HTTP
    response = requests.get(url)

    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Parsear o HTML da página
        soup = BeautifulSoup(response.content, "html.parser")

        # Encontrar o elemento <option> com o valor desejado
        option_element = soup.find("option", value="HORARIO")

        # Se o elemento foi encontrado, extrair o valor de data-url
        if option_element:
            data_url = option_element.get("data-url")
            st.info(f"URL encontrada: {data_url}")
        else:
            st.error("Elemento <option> não encontrado.")
    else:
        st.error(f"Erro ao acessar o site: {response.status_code}")

    # URL do arquivo
    url = data_url

    # st.info(f"Diretório atual: {os.getcwd()}")
    # Criar diretório se não existir

    raw_data_dir = "./data/bruto"
    if not os.path.exists(raw_data_dir):
        os.makedirs(raw_data_dir)

    # Nome do arquivo para salvar
    filename = f"{raw_data_dir}/Historico_do_Preco_Horario.xlsx"

    # Fazer o download
    response = requests.get(url)

    # Verificar se o download foi bem-sucedido
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        st.success(f"Arquivo salvo como {filename}")
    else:
        st.error(f"Erro ao baixar o arquivo: {response.status_code}")

    return st.success("Arquivo salvo com sucesso")


def clean_pld_data():
    # st.info(f"Diretório atual: {os.getcwd()}")
    excel_path = "./data/bruto/Historico_do_Preco_Horario.xlsx"
    df = pd.ExcelFile(excel_path)
    data = df.parse(sheet_name=df.sheet_names[0])
    data_melted = data.melt(
        id_vars=["Hora", "Submercado"],  # Colunas que permanecem como identificadores
        var_name="Data",  # Nome para a nova coluna que conterá os nomes das colunas originais (datas)
        value_name="Valor",  # Nome para a nova coluna que conterá os valores das colunas originais
    )
    data.dropna(inplace=True)

    # Criar diretório se não existir
    clean_data_dir = "./data/limpo"
    if not os.path.exists(clean_data_dir):
        os.makedirs(clean_data_dir)

    data_melted.to_csv(
        f"{clean_data_dir}/dados_{datetime.datetime.utcnow().strftime('%Y-%m-%d')}.csv",
        index=False,
    )

    return st.success("Dados limpos com sucesso.")


def get_latest_clean_data_file():
    clean_data_dir = "./data/limpo"
    files = [
        f
        for f in os.listdir(clean_data_dir)
        if f.startswith("dados_") and f.endswith(".csv")
    ]
    if not files:
        raise FileNotFoundError("Nenhum arquivo de dados encontrado.")
    latest_file = max(
        files, key=lambda x: datetime.datetime.strptime(x, "dados_%Y-%m-%d.csv")
    )
    return os.path.join(clean_data_dir, latest_file)
