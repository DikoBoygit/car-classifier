import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms
import os

# --- 1. КОНФИГУРАЦИЯ ---
DATA_DIR = '../data'
MODEL_SAVE_PATH = 'models/best_model.pth'
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
BATCH_SIZE = 32
LEARNING_RATE = 0.001
EPOCHS = 10

print(f"Используемое устройство: {DEVICE}")
os.makedirs('models', exist_ok=True) # Создаём папку models, если её нет

# --- 2. ТРАНСФОРМАЦИИ И ДАННЫЕ ---
# Трансформации для изображений (обучение и валидация)
data_transforms = {
    'train': transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
    'val': transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
}

# Загружаем данные с помощью ImageFolder
full_dataset = datasets.ImageFolder(DATA_DIR)

# Делим данные: 80% на обучение, 20% на валидацию
train_size = int(0.8 * len(full_dataset))
val_size = len(full_dataset) - train_size
train_dataset, val_dataset = torch.utils.data.random_split(full_dataset, [train_size, val_size])

# Применяем нужные трансформации к каждой части
train_dataset.dataset.transform = data_transforms['train']
val_dataset.dataset.transform = data_transforms['val']

# Создаём загрузчики данных
dataloaders = {
    'train': DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True),
    'val': DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=True)
}
class_names = full_dataset.classes
print(f"Найдены классы: {class_names}")

# --- 3. ОПРЕДЕЛЕНИЕ МОДЕЛИ ---
model = models.resnet34(weights=models.ResNet34_Weights.IMAGENET1K_V1)
for param in model.parameters():
    param.requires_grad = False

num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, len(class_names)) # 2 выхода: damaged и whole
model = model.to(DEVICE)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.fc.parameters(), lr=LEARNING_RATE)

# --- 4. ЦИКЛ ОБУЧЕНИЯ ---
best_acc = 0.0
for epoch in range(EPOCHS):
    print(f'Эпоха {epoch+1}/{EPOCHS}')
    print('-' * 10)

    for phase in ['train', 'val']:
        if phase == 'train':
            model.train()
        else:
            model.eval()

        running_loss = 0.0
        running_corrects = 0

        for inputs, labels in dataloaders[phase]:
            inputs = inputs.to(DEVICE)
            labels = labels.to(DEVICE)

            optimizer.zero_grad()

            with torch.set_grad_enabled(phase == 'train'):
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                loss = criterion(outputs, labels)

                if phase == 'train':
                    loss.backward()
                    optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)

        epoch_loss = running_loss / len(dataloaders[phase].dataset)
        epoch_acc = running_corrects.double() / len(dataloaders[phase].dataset)

        print(f'{phase} Потери: {epoch_loss:.4f} Точность: {epoch_acc:.4f}')

        if phase == 'val' and epoch_acc > best_acc:
            best_acc = epoch_acc
            torch.save(model.state_dict(), MODEL_SAVE_PATH)
            print(f"✅ Новая лучшая модель сохранена с точностью {best_acc:.4f}")

print(f'\nОбучение завершено. Лучшая точность: {best_acc:4f}')