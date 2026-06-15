from pydantic import BaseModel, ConfigDict

class ItemCreate(BaseModel):
    hanzi: str
    pinyin: str
    english: str
    img_url: str

class Item(ItemCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int