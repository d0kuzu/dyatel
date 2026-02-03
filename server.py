from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

# Папка для хранения загруженных файлов
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Доступ к файлам через браузер
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Эндпоинт для загрузки
@app.post("/upload")
async def upload_photo(photo: UploadFile = File(...)):
    file_path = UPLOAD_DIR / photo.filename
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
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)