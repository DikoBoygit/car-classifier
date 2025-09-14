from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .model import get_prediction
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Car Damage Detection API")

# Настройка CORS, чтобы разрешить запросы от твоего фронтенда
origins = [
    "http://localhost",
    "http://localhost:3000", # Стандартный порт для React-приложений
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """Корневой эндпоинт для проверки работы сервера."""
    return {"message": "API для определения состояния автомобиля работает"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """Эндпоинт для предсказания состояния автомобиля по фото."""
    logger.info(f"Получен файл: {file.filename}")
    
    # Проверяем, что файл - это изображение
    if not file.content_type.startswith("image/"):
        logger.warning(f"Загружен неверный тип файла: {file.content_type}")
        raise HTTPException(status_code=400, detail="Неверный тип файла. Пожалуйста, загрузите изображение.")

    try:
        # Читаем содержимое файла в байты
        image_bytes = await file.read()
        
        # Получаем предсказание от модели
        prediction = get_prediction(image_bytes)
        logger.info(f"Результат предсказания: {prediction}")
        
        return prediction
    except Exception as e:
        logger.error(f"Произошла ошибка при обработке файла: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера при обработке изображения.")
