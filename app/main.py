from fastapi import FastAPI
from app.routes.leyendas import router as leyendas_router

app = FastAPI()

app.include_router(leyendas_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}