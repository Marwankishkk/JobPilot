from fastapi import FastAPI
from core.db import Base, engine
from routes.user import router as user_router

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(user_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to JobPilot!"}

