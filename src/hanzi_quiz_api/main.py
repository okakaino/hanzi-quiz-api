import random

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.orm import Session

from hanzi_quiz_api.models import ItemCreate, Item, QuizAnswer
from hanzi_quiz_api.database import Base, engine, get_db, ItemDB

from hanzi_quiz_api.quiz import check_answer

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
def read_root():
    return {"status": "ok"}

@app.get('/quiz')
def get_quiz(db: Session = Depends(get_db)):
    items = db.scalars(select(ItemDB)).all()

    if len(items) < 3:
        raise HTTPException(400, 'Need at least 3 items to build a quiz')
    
    correct, d1, d2 = random.sample(items, 3)

    hanzi_options = random.sample([correct.hanzi, d1.hanzi, d2.hanzi], 3)
    pinyin_options = random.sample([correct.pinyin, d1.pinyin, d2.pinyin], 3)

    return {
        'item_id': correct.id,
        'img_url': correct.img_url,
        'hanzi_options': hanzi_options,
        'pinyin_options': pinyin_options
    }

@app.post('/quiz/check')
def check_quiz(answer: QuizAnswer, db:Session = Depends(get_db)):
    item = db.get(ItemDB, answer.item_id)

    if item is None:
        raise HTTPException(status_code=404, detail='Item not found')
    
    return check_answer(item.hanzi, item.pinyin, answer.hanzi_option, answer.pinyin_option)

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