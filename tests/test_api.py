import os

import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from hanzi_quiz_api.main import app
from hanzi_quiz_api.database import Base, get_db

client = TestClient(app=app)

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg://ted@localhost:5432/hanzi_test",  # safe default, no secret
)
test_engine = create_engine(TEST_DATABASE_URL)
TestSession = sessionmaker(bind=test_engine)

def test_read_root():
    response = client.get('/')

    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}

def override_get_db():
    db = TestSession()

    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def fresh_tables():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

def test_create_item():
    response = client.post('/items', json={
        "hanzi": "狗", "pinyin": "gǒu", "english": "dog", "img_url": ""
    })

    assert response.status_code == 201

    data = response.json()

    assert data["hanzi"] == "狗"
    assert 'id' in data

def test_get_item():
    response = client.post('/items', json={
        "hanzi": "狗", "pinyin": "gǒu", "english": "dog", "img_url": ""
    })

    quiz1 = client.get('/items/1')
    assert quiz1.status_code == 200
    assert quiz1.json()['id'] == 1

    quiz_none = client.get('/items/99')
    assert quiz_none.status_code == 404

def test_get_quiz():
    data1 = client.get('/quiz')
    assert data1.status_code == 400

    client.post('/items', json={
        "hanzi": "狗", "pinyin": "gǒu", "english": "dog", "img_url": ""
    })
    client.post('/items', json={
        "hanzi": "苹果", "pinyin": "píngguǒ", "english": "apple", "img_url": ""
    })
    client.post('/items', json={
        "hanzi": "水", "pinyin": "shuǐ", "english": "water", "img_url": ""
    })

    data2 = client.get('/quiz')

    assert data2.status_code == 200
    assert data2.json()['item_id'] is not None
    assert "狗" in data2.json()['hanzi_options']
    assert "苹果" in data2.json()['hanzi_options']
    assert "水" in data2.json()['hanzi_options']
    assert "gǒu" in data2.json()['pinyin_options']
    assert "píngguǒ" in data2.json()['pinyin_options']
    assert "shuǐ" in data2.json()['pinyin_options']

def test_check_quiz():
    client.post('/items', json={
        "hanzi": "狗", "pinyin": "gǒu", "english": "dog", "img_url": ""
    })
    client.post('/items', json={
        "hanzi": "苹果", "pinyin": "píngguǒ", "english": "apple", "img_url": ""
    })
    client.post('/items', json={
        "hanzi": "水", "pinyin": "shuǐ", "english": "water", "img_url": ""
    })

    response1 = client.post('/quiz/check', json={
        'item_id': 1,
        'hanzi_option': '狗',
        'pinyin_option': 'gǒu'
    })

    assert response1.status_code == 200
    assert response1.json() == {
        'hanzi_correct': True,
        'pinyin_correct': True
    }

    response2 = client.post('/quiz/check', json={
        'item_id': 5,
        'hanzi_option': '狗',
        'pinyin_option': 'gǒu'
    })

    assert response2.status_code == 404

    response3 = client.post('/quiz/check', json={
        'item_id': 2,
        'hanzi_option': '苹果',
        'pinyin_option': 'gǒu'
    })

    assert response3.status_code == 200
    assert response3.json() == {
        'hanzi_correct': True,
        'pinyin_correct': False
    }

    response4 = client.post('/quiz/check', json={
        'item_id': 2,
        'hanzi_option': '狗',
        'pinyin_option': 'píngguǒ'
    })

    assert response4.status_code == 200
    assert response4.json() == {
        'hanzi_correct': False,
        'pinyin_correct': True
    }