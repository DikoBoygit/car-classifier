// frontend/src/App.js

import React, { useState, useRef } from 'react';
import './App.css';
import carIcon from './car-icon.png'; // Скачай иконку и положи в папку src

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setError('');
      setResult(null);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Пожалуйста, выберите файл для загрузки.');
      return;
    }

    setIsLoading(true);
    setError('');
    setResult(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://127.0.0.1:8000/predict', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Ошибка сети или сервера. Убедитесь, что бэкенд запущен.');
      }

      const data = await response.json();
      setResult(data);

    } catch (err) {
      setError(err.message || 'Произошла ошибка. Убедитесь, что бэкенд-сервер запущен и отвечает.');
    } finally {
      setIsLoading(false);
    }
  };

  // Позволяет кликать на блок и открывать выбор файла
  const onAreaClick = () => {
    fileInputRef.current.click();
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <img src={carIcon} alt="Иконка автомобиля" className="header-icon" />
        <h1>Определение состояния автомобиля</h1>
        <p>Загрузите фотографию для анализа целостности кузова.</p>
      </header>

      <main className="app-main">
        <div className="card upload-card">
          <input
            type="file"
            onChange={handleFileChange}
            accept="image/*"
            ref={fileInputRef}
            style={{ display: 'none' }}
          />
          <div className="upload-area" onClick={onAreaClick}>
            {preview ? (
              <img src={preview} alt="Предпросмотр" className="image-preview" />
            ) : (
              <p>Нажмите здесь или перетащите фото для загрузки</p>
            )}
          </div>
          <button onClick={handleUpload} disabled={isLoading || !selectedFile} className="check-button">
            {isLoading ? 'Анализ...' : 'Проверить'}
          </button>
        </div>

        {error && <p className="error-message">{error}</p>}

        {isLoading && (
            <div className="card loading-card">
                <div className="loader"></div>
                <p>Анализируем ваше фото...</p>
            </div>
        )}

        {result && (
          <div className="card result-card">
            <h2>Результат анализа:</h2>
            <p className={result.integrity === 'Битый' ? 'result-damaged' : 'result-whole'}>
              Состояние: <strong>{result.integrity}</strong>
            </p>
            <p>Уверенность: <strong>{result.confidence}</strong></p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;