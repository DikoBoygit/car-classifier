# Определение состояния автомобиля по фотографиям 🚗

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-05998b?logo=fastapi) ![React](https://img.shields.io/badge/React-blue?logo=react&logoColor=61DAFB) ![GitHub](https://img.shields.io/badge/GitHub-repo-blue?logo=github)

Веб-приложение для анализа целостности кузова автомобиля по фотографии с использованием нейронной сети.

---
### **Как это выглядит**
![Изображение WhatsApp 2025-09-14 в 19 13 41_c4c19c88](https://github.com/user-attachments/assets/173481ef-7b97-4926-86ec-6597c4bc7c12)


---

## 🛠️ Технологии

* **Бэкенд**: Python, FastAPI, PyTorch, Uvicorn
* **Фронтенд**: JavaScript, React, HTML/CSS

---

## 📊 Данные

Модель обучалась на датасетах, содержащих изображения поврежденных и целых автомобилей. Основные источники данных:

* **Наборы данных с Roboflow:**
    * [Rust and Scrach](https://universe.roboflow.com/seva-at1qy/rust-and-scrach)
    * [Car Scratch and Dent](https://universe.roboflow.com/carpro/car-scratch-and-dent)
    * [Car Scratch](https://universe.roboflow.com/project-kmnth/car-scratch-xgxzs)
* **Набор данных с Kaggle:**
    * [Cars Image Dataset](https://www.kaggle.com/datasets/kshitij192/cars-image-dataset)

---

## ⚙️ Установка и запуск

### **1. Предварительные требования**

Убедитесь, что у вас установлены **Python 3.8+**, **Node.js (с npm)** и **Git**.

### **2. Клонирование и настройка**

```bash
# Клонируйте репозиторий
git clone [https://github.com/DikoBoygit/car-classifier.git](https://github.com/DikoBoygit/car-classifier.git)

# Перейдите в папку проекта
cd car-classifier
```

### **3. Загрузка данных для предсказаний**

Модель требует датасет, который не хранится в репозитории.
1.  **Скачайте архив `data`** по [**этой ссылке**]([https://drive.google.com/drive/u/1/folders/1_TpC4axo4z35dF8Acy1mXt_S1xf4A3rZ](https://drive.google.com/drive/folders/1_TpC4axo4z35dF8Acy1mXt_S1xf4A3rZ?usp=sharing)).
2.  **Распакуйте** его и поместите папку `data` в корень проекта.

### **4. Настройка Бэкенда**

```bash
# Перейдите в папку бэкенда
cd backend

# Создайте и активируйте виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt
```

### **5. Настройка Фронтенда**

```bash
# Перейдите в папку фронтенда
cd ../frontend

# Установите зависимости
npm install
```

---

## 🚀 Запуск приложения

> **Важно:** Бэкенд и фронтенд должны быть запущены одновременно в двух разных терминалах.

1.  **Запуск Бэкенда (Терминал 1):**
    ```bash
    # В корневой папке проекта (`car-classifier`)
    uvicorn backend.app.main:app --reload
    ```

2.  **Запуск Фронтенда (Терминал 2):**
    ```bash
    # В папке /frontend
    npm start
    ```
Приложение будет доступно по адресу `http://localhost:3000`.
