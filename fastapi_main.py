from fastapi import FastAPI
from routes.detetect_routes import detection

app = FastAPI()

app.include_router(detection)
