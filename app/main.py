# from fastapi import FastAPI, Depends
# from sqlalchemy.orm import Session
# from .db import SessionLocal, engine
# from .models import Base
# from .crud import get_items, create_item

# Base.metadata.create_all(bind=engine)

# app = FastAPI()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @app.get("/items")
# def list_items(db: Session = Depends(get_db)):
#     return get_items(db)

# @app.post("/items")
# def add_item(name: str, db: Session = Depends(get_db)):
#     return create_item(db, name)

from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Item
import httpx

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD endpoint
@app.post("/items")
def create_item(name: str, db: Session = Depends(get_db)):
    item = Item(name=name)
    db.add(item)
    db.commit()
    db.refresh(item)

    # Trigger webhook callback
    try:
        # Replace with real URL if testing externally
        httpx.post("http://localhost:8080/webhook", json={"event": "item_created", "item": item.name, "id": item.id})
    except Exception as e:
        print("Webhook failed:", e)

    return {"id": item.id, "name": item.name}

@app.get("/items")
def read_items(db: Session = Depends(get_db)):
    return db.query(Item).all()

# Webhook endpoint
@app.post("/webhook")
async def webhook_receiver(request: Request):
    data = await request.json()
    print("Webhook received:", data)
    return {"status": "received"}
