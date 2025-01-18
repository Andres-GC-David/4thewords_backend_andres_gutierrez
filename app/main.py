from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

app.mount("/imagenes", StaticFiles(directory="imagenes"), name="imagenes")

@app.get("/")
async def root():
    return {"message": "Hello World"}