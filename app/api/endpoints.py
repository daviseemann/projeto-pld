from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import requests
from datetime import datetime

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
