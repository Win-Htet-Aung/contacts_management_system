from sqlalchemy.orm import Session
from ..models import Item as ItemModel
from ..schemas import Item as ItemSchema


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ItemModel.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: ItemSchema.ItemCreate, user_id: int):
    db_item = ItemModel.Item(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
