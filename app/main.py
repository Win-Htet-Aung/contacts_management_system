from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .repository import User as UserRepository, Item as ItemRepository
from .schemas import User as UserSchema, Item as ItemSchema
from .settings.database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=UserSchema.User)
def create_user(user: UserSchema.UserCreate, db: Session = Depends(get_db)):
    db_user = UserRepository.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return UserRepository.create_user(db=db, user=user)


@app.get("/users/", response_model=list[UserSchema.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = UserRepository.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=UserSchema.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = UserRepository.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=ItemSchema.Item)
def create_item_for_user(
    user_id: int, item: ItemSchema.ItemCreate, db: Session = Depends(get_db)
):
    return ItemRepository.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[ItemSchema.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = ItemRepository.get_items(db, skip=skip, limit=limit)
    return items
