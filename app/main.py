from fastapi import FastAPI

from app.controller.api import router

app = FastAPI(
    title="FastAPI + MongoDB",
    docs_url="/"
)

app.include_router(router)