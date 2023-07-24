import os
import uuid

from fastapi import FastAPI

from src.routes import routes
from src.core.db import engine
from src.core.base import Base
from arq_dashboard import app as app_arq_dashboard
from arq_dashboard.api.api import api_router

app = FastAPI()


@app.on_event("startup")
async def startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown() -> None:
    async def shutdown_event():
        pass



app.include_router(routes)

app.include_router(api_router, prefix="/api", tags=["queue"])

app.mount(
    "/", app_arq_dashboard
)