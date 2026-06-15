from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Depends

from sqlalchemy import select

from sqlalchemy.orm import Session

from hanzi_quiz_api.models import ItemCreate, Item

from hanzi_quiz_api.database import Base, engine, get_db, ItemDB

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
def read_root():
    return {"status": "ok"}

@app.get('/items')
def list_items(db: Session = Depends(get_db)) -> list[Item]:
    return db.scalars(select(ItemDB)).all()

@app.post('/items', status_code=201)
def create_item(payload: ItemCreate, db: Session = Depends(get_db)) -> Item:
    db_item = ItemDB(**payload.model_dump())

    db.add(db_item)

    db.commit()

    db.refresh(db_item)

    return db_item

@app.get('/items/{item_id}')
def get_item(item_id: int, db: Session = Depends(get_db)) -> Item:
    item = db.get(ItemDB, item_id)

    if item is None:
        raise HTTPException(status_code=404, detail='Item not found')
    
    return item