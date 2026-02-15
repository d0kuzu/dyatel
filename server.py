import time

from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Папка для хранения загруженных файлов
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Serve the frontend
@app.get("/")
async def read_index():
    return FileResponse('frontend/index.html')

# Доступ к файлам через браузер
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Эндпоинт для загрузки
@app.post("/upload")
async def upload_photo(photo: UploadFile = File(...)):
    file_path = UPLOAD_DIR / f"{int(time.time())}.png"
    contents = await photo.read()
    with open(file_path, "wb") as f:
        f.write(contents)
    return {"filename": photo.filename}

# Эндпоинт для списка всех загруженных файлов
@app.get("/photos")
def list_photos():
    return {"photos": [f"/uploads/{f.name}" for f in UPLOAD_DIR.iterdir() if f.is_file()]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8002, reload=True)