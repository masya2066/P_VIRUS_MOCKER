from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from src.database.database import Database
from src.api.router import router
from src.config.init import InitConfig, set_env_from_config
from dotenv import load_dotenv
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    config = InitConfig()
    set_env_from_config(config)
    yield
    # Any cleanup code can go here

app = FastAPI()
app.include_router(router, prefix="")
db = Database()


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == '__main__':
    print(db)
    uvicorn.run("main:app", host='127.0.0.1',
                port=int(os.getenv("SERVER_PORT")), reload=True, workers=20)
