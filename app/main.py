from fastapi import FastAPI
from app.database import engine, Base
from app.api import endpoints
from app.models import (
    PLDData,
)  # Importar o modelo para garantir que a tabela seja criada

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# Configuração do banco de dados
Base.metadata.create_all(bind=engine)  # Certifique-se de que a tabela seja criada

# Incluir os endpoints da API
app.include_router(endpoints.router)
