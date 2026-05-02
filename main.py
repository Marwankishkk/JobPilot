from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.db import Base, engine
from routes.user import router as user_router
from routes.job import router as job_router
Base.metadata.create_all(bind=engine)
origins = [
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "https://localhost:3001",
    "https://localhost:3000",
    "https://job-pilot-front-end-dvr1.vercel.app/",
]

app = FastAPI()

app.include_router(user_router)
app.include_router(job_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"message": "Welcome to JobPilot!"}

