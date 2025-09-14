import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import io
import os

# --- 1. КОНФИГУРАЦИЯ ---
# Убедись, что этот путь правильный относительно места запуска uvicorn
MODEL_PATH = 'backend/models/best_model.pth' 
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

# ВАЖНО: Имена классов должны быть в том же порядке, в котором их нашел PyTorch
# PyTorch сортирует папки по алфавиту: 'damaged', 'whole'
CLASS_NAMES = ['damaged', 'whole'] 
# Переводим на русский для вывода
CLASS_NAMES_RU = {'damaged': 'Битый', 'whole': 'Целый'}

# --- 2. ЗАГРУЗКА МОДЕЛИ ---
# Загружаем ту же архитектуру, что и при обучении
model = models.resnet34(weights=None) # Веса загрузим свои

# Заменяем последний слой, чтобы он соответствовал нашей задаче (2 класса)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, len(CLASS_NAMES))

# Загружаем сохранённые веса из файла
# map_location=DEVICE гарантирует, что модель загрузится на CPU, если нет GPU
if os.path.exists(MODEL_PATH):
    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    print(f"Модель '{MODEL_PATH}' успешно загружена.")
else:
    print(f"ВНИМАНИЕ: Файл модели '{MODEL_PATH}' не найден. Предсказания будут случайными.")
    # Это заглушка на случай, если модель еще не обучена
    model = None 

# Переводим модель в режим предсказания
if model:
    model.to(DEVICE)
    model.eval()

# --- 3. ТРАНСФОРМАЦИИ ИЗОБРАЖЕНИЯ ---
# Применяем те же трансформации, что и при валидации в train.py
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# --- 4. ФУНКЦИЯ ПРЕДСКАЗАНИЯ ---
def get_prediction(image_bytes: bytes) -> dict:
    if not model:
        return {"integrity": "Модель не обучена", "confidence": 0.0}

    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image_tensor = transform(image).unsqueeze(0).to(DEVICE)

        # Получаем предсказание от модели
        with torch.no_grad():
            outputs = model(image_tensor)
            # Применяем Softmax, чтобы получить вероятности
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            # Находим класс с максимальной вероятностью
            confidence, predicted_idx = torch.max(probabilities, 1)
            
            predicted_class = CLASS_NAMES[predicted_idx.item()]
            integrity_ru = CLASS_NAMES_RU[predicted_class]

        return {
            "integrity": integrity_ru, 
            "confidence": f"{confidence.item():.2f}"
        }

    except Exception as e:
        print(f"Ошибка при предсказании: {e}")
        return {"error": "Не удалось обработать изображение."}
