from fastapi import FastAPI
from app.core.config import settings
from app.api.auth import auth_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)
app.include_router(router=auth_router)

@app.get("/")
def home() -> dict:
    return {
        "message":settings.APP_NAME,
        "version":settings.APP_VERSION,
        "debug":settings.DEBUG
    }