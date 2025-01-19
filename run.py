import os
import uvicorn
from fastapi.staticfiles import StaticFiles
from app.main import app

IMAGENES_DIR = os.path.join(os.path.dirname(__file__), "imagenes")

app.mount("/imagenes", StaticFiles(directory=IMAGENES_DIR), name="imagenes")

def main():
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("app.main:app", host="127.0.0.1", port=port, reload=True)

if __name__ == "__main__":
    main()
