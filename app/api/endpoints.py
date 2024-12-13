from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import requests
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup

from app import models, schemas, database

router = APIRouter()


@router.get("/update_pld")
def update_pld(db: Session = Depends(database.get_db)):
    response = requests.get("https://api.ccee.org.br/pld")
    if response.status_code == 200:
        data = response.json()
        for entry in data:
            pld = models.PLDData(
                id=f"{entry['submarket']}_{entry['timestamp']}",
                submarket=entry["submarket"],
                price=entry["price"],
                timestamp=datetime.strptime(entry["timestamp"], "%Y-%m-%dT%H:%M:%S"),
            )
            db.merge(pld)
        db.commit()
    return {"status": "Dados atualizados com sucesso"}


@router.get("/pld/{submarket}", response_model=list[schemas.PLDDataSchema])
def get_pld(
    submarket: str,
    start_date: str,
    end_date: str,
    db: Session = Depends(database.get_db),
):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    results = (
        db.query(models.PLDData)
        .filter(
            models.PLDData.submarket == submarket,
            models.PLDData.timestamp >= start,
            models.PLDData.timestamp <= end,
        )
        .all()
    )
    return results


@router.get("/download_pld")
def download_pld(db: Session = Depends(database.get_db)):

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
            print(f"URL encontrada: {data_url}")
        else:
            print("Elemento <option> não encontrado.")
    else:
        print(f"Erro ao acessar o site: {response.status_code}")

    # URL do arquivo
    url = data_url
    # Nome do arquivo para salvar
    filename = "Historico_do_Preco_Horario.xlsx"

    # Fazer o download
    response = requests.get(url)

    # Verificar se o download foi bem-sucedido
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"Arquivo salvo como {filename}")
    else:
        print(f"Erro ao baixar o arquivo: {response.status_code}")

        return {"status": "Arquivo gerado com sucesso"}


@router.get("/clean_pld_data")
def clean_pld_data(db: Session = Depends(database.get_db)):
    excel_path = "../data/Historico_do_Preco_Horario_-_17_de_abril_de_2018_a_6_de_novembro_de_2024.xlsx"
    df = pd.ExcelFile(excel_path)
    data = df.parse(sheet_name=df.sheet_names[0])
    data.dropna(inplace=True)
    data_melted = data.melt(
        id_vars=["Hora", "Submercado"],  # Colunas que permanecem como identificadores
        var_name="Data",  # Nome para a nova coluna que conterá os nomes das colunas originais (datas)
        value_name="Valor",  # Nome para a nova coluna que conterá os valores das colunas originais
    )

    data_melted.to_csv("../data/clean_data.csv", index=False)
    return {"status": "Dados apagados com sucesso"}
