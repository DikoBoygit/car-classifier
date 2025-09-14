# Определение состояния автомобиля по фотографиям 🚗

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-black?logo=flask&logoColor=white) ![React](https://img.shields.io/badge/React-blue?logo=react&logoColor=61DAFB) ![GitHub](https://img.shields.io/badge/GitHub-repo-blue?logo=github)

Веб-приложение для анализа целостности кузова автомобиля по фотографии с использованием нейронной сети.

---

## 🛠️ Технологии

* **Бэкенд**: Python, Flask, TensorFlow/Keras, Pillow
* **Фронтенд**: JavaScript, React, HTML/CSS

---

## ⚙️ Установка и запуск

### **1. Предварительные требования**

Убедитесь, что у вас установлены **Python 3.8+**, **Node.js (с npm)** и **Git**.

### **2. Клонирование и настройка**

```bash
# Клонируйте репозиторий
git clone https://github.com/DikoBoygit/car-classifier.git

# Перейдите в папку проекта
cd car-classifier
```

### **3. Загрузка данных**

Модель требует датасет, который не хранится в репозитории.
1.  **Скачайте архив `data`** по [**этой ссылке**](https://drive.google.com/drive/u/1/folders/1_TpC4axo4z35dF8Acy1mXt_S1xf4A3rZ).
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
    # В папке /backend с активным venv
    python3 app/main.py
    ```

2.  **Запуск Фронтенда (Терминал 2):**
    ```bash
    # В папке /frontend
    npm start
    ```
Приложение будет доступно по адресу `http://localhost:3000`.
