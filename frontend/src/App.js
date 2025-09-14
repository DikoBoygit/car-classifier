import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreview(URL.createObjectURL(file));
      setResult(null);
      setError('');
    }
  };

  const handleSubmit = async () => {
    if (!selectedFile) {
      setError('Пожалуйста, выберите файл.');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    setLoading(true);
    setError('');
    setResult(null);

    try {
      // Убедись, что URL правильный! Это адрес твоего бэкенд-сервера.
      const response = await axios.post('http://127.0.0.1:8000/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResult(response.data);
    } catch (err) {
      setError('Произошла ошибка. Убедитесь, что бэкенд-сервер запущен и отвечает.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <h1>Определение состояния автомобиля 🚗</h1>
        <p>Загрузите фотографию для анализа целостности кузова.</p>
        
        <div className="uploader-card">
          <input id="file-upload" type="file" accept="image/*" onChange={handleFileChange} />
          <button onClick={handleSubmit} disabled={loading || !selectedFile}>
            {loading ? 'Анализ...' : 'Проверить'}
          </button>
        </div>

        {error && <p className="error-message">{error}</p>}

        <div className="content-area">
          {preview && (
            <div className="card">
              <h3>Ваше фото:</h3>
              <img src={preview} alt="Загруженное изображение" />
            </div>
          )}

          {result && !result.error && (
            <div className="card result-card">
              <h3>Результат анализа:</h3>
              <p>
                <strong>Состояние:</strong> 
                <span className={result.integrity === 'Битый' ? 'damaged' : 'whole'}>
                  {result.integrity}
                </span>
              </p>
              <p>
                <strong>Уверенность:</strong> {result.confidence}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;

