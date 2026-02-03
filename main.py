from PIL import ImageGrab
import keyboard
import io
import requests

ENDPOINT = "http://localhost:8000/upload"  # должен совпадать с FastAPI

def send_screenshot():
    # делаем скриншот
    img = ImageGrab.grab()

    # сохраняем в байты
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    # отправка POST с файлом под ключом 'photo'
    files = {'photo': ('screenshot.png', buf, 'image/png')}
    try:
        response = requests.post(ENDPOINT, files=files)
        print(f"Отправлено! Статус: {response.status_code}")
        print(response.json())
    except Exception as e:
        print(f"Ошибка при отправке: {e}")

print("Нажми F8 для отправки скриншота. Esc — выход.")

keyboard.add_hotkey("F8", send_screenshot)
keyboard.wait("esc")
