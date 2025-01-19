from fastapi import FastAPI
from app.routes.leyendas import router as leyendas_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


app.include_router(leyendas_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}