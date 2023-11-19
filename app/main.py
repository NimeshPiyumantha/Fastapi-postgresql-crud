from fastapi import FastAPI
import model
from routes import router
from config import engine

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router, prefix="/book", tags=["book"])

