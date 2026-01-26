from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Item
import httpx
from fastapi import HTTPException
from contextlib import asynccontextmanager
##
from prometheus_fastapi_instrumentator import Instrumentator

##
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

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
        httpx.post("https://webhook.site/30cc039a-3e58-4e74-83f9-4860406ff233", json={"event": "item_created", "item": item.name, "id": item.id})
    except Exception as e:
        print("Webhook failed:", e)

    return {"id": item.id, "name": item.name}

@app.get("/items")
def read_items(db: Session = Depends(get_db)):
    return db.query(Item).all()
@app.get("/health")
def health():
    return {"status": "ok"}

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"status": "deleted"}

@app.put("/items/{item_id}")
def update_item(item_id: int, name: str, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.name = name
    db.commit()
    db.refresh(item)
    # Trigger webhook callback
    try:
        # Replace with real URL if testing externally
        httpx.post("https://webhook.site/30cc039a-3e58-4e74-83f9-4860406ff233", json={"event": "item_updated", "item": item.name, "id": item.id})
    except Exception as e:
        print("Webhook failed:", e)

    return {"id": item.id, "name": item.name} 


# Webhook endpoint
@app.post("/webhook")
async def webhook_receiver(request: Request):
    data = await request.json()
    print("Webhook received:", data)
    return {"status": "received"}

##
Instrumentator().instrument(app).expose(app)
##


