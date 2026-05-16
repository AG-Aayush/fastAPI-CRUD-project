from fastapi import FastAPI
from app.routes import router, auth_router
from app.db import engine, Base

app = FastAPI(title='FastAPI CRUD API')


app.include_router(auth_router)
app.include_router(router)

@app.on_event("startup")
async def standard():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def home():
    return {"message": "FastAPI CRUD Running"}