
# Plate Recognition

## Описание
Этот проект предназначен для распознавания номерных знаков с использованием YOLO и TrOCR. Система состоит из:
1. Сервиса обработки видео/изображений и записи результатов в PostgreSQL.
2. API-сервиса для взаимодействия с базой данных.

---

## Установка

### 1. Клонирование репозитория
```bash
git clone https://github.com/oldrzym/plate_recognition.git
cd plate_recognition
```

### 2. Переключение на ветку `dev` (для разработки)
```bash
git checkout dev
```

---

## Использование

### **Test**
1. Переименуйте файл `.env.example` в `.env` и настройте переменные окружения, если требуется.
2. Запустите Docker Compose:
   ```bash
   docker-compose up --build
   ```
3. Доступ к эндпоинтам:
   - JSON с последней записью: [http://localhost:8000/last-record](http://localhost:8000/last-record)
   - Картинка последней записи: [http://localhost:8000/last-record/image](http://localhost:8000/last-record/image)

---

### **Prod**
1. В файле `.env` замените:
   ```plaintext
   ENV=dev
   ```
   на:
   ```plaintext
   ENV=prod
   ```,
   а также 
      ```plaintext
   VIDEO_SOURCE=rtsp://192.168.1.100:554/stream
   ``` на актуальный адрес видеокамеры
2. Запустите Docker Compose:
   ```bash
   docker-compose up --build
   ```
3. В режиме `prod` сервис подключается к камере, указанной в переменной окружения `VIDEO_SOURCE`, и записывает данные при обнаружении одинаковых номеров.

---

## Дополнительно
### 1. Переменные окружения:
   - `ENV` – Режим работы (`dev` или `prod`).
   - `VIDEO_SOURCE` – Источник видео (камера или тестовое изображение).
   - `NUMBER_BUFFER_SIZE` – Количество повторений номера для записи в базу данных.
   - `POSTGRES_HOST` – Хост PostgreSQL.
   - `POSTGRES_PORT` – Порт PostgreSQL.
   - `POSTGRES_USER` – Пользователь PostgreSQL.
   - `POSTGRES_PASSWORD` – Пароль PostgreSQL.
   - `POSTGRES_DB` – База данных PostgreSQL.

### 2. Проверка базы данных:
Чтобы подключиться к PostgreSQL, выполните:
```bash
docker exec -it postgres psql -U user -d app_db
```
SQL-запрос для просмотра записей:
```sql
SELECT * FROM vehicle_numbers;
```

### 3. Основные эндпоинты:
- **Получить последнюю запись:**
  ```plaintext
  GET /last-record
  ```
- **Получить картинку последней записи:**
  ```plaintext
  GET /last-record/image
  ```
- **Получить записи за определённый период:**
  ```plaintext
  GET /records?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
  ```
---
