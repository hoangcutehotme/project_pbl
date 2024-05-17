from fastapi import FastAPI
from routes.detetect import detection

app = FastAPI()

app.include_router(detection)