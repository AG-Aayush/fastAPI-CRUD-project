from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes import router, auth_router
from app.db import engine, Base
from fastapi.responses import RedirectResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    # runs on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # runs on shutdown (nothing needed here)

app = FastAPI(title='FastAPI CRUD API', lifespan=lifespan)

app.include_router(auth_router)
app.include_router(router)

@app.get("/")
async def home():
    return RedirectResponse(url="/docs")