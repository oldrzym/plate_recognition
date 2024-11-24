
# Plate Recognition

Проект для распознавания номерных знаков с использованием Nomeroff-Net, PostgreSQL и FastAPI. Основная цель — обработка видеопотока, распознавание автомобильных номерных знаков и сохранение данных в базе данных PostgreSQL. Проект также предоставляет REST API для взаимодействия с данными.

## 📂 Структура проекта

```
plate_recognition/
├── Dockerfile                 # Dockerfile для video_processor
├── Dockerfile.api             # Dockerfile для API
├── docker-compose.yml         # Docker Compose для запуска сервисов
├── init.sql                   # Скрипт инициализации базы данных PostgreSQL
├── requirements.txt           # Зависимости для video_processor
├── requirements-api.txt       # Зависимости для API
├── main.py                    # Основная логика обработки видеопотока
├── api.py                     # Реализация REST API
├── nomeroff_processor.py      # Логика распознавания номерных знаков с помощью Nomeroff-Net
├── postgres_client.py         # Класс для работы с PostgreSQL
├── .env                       # Файл с переменными окружения
└── README.md                  # Документация проекта
```

## 🚀 Установка и запуск

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/oldrzym/plate_recognition.git
cd plate_recognition
```

### 2. Создайте и настройте файл `.env`
Создайте файл `.env` в корне проекта и добавьте следующие переменные окружения:

```env
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=app_db
ENV=prod
```

### 3. Запустите проект с Docker Compose
Убедитесь, что у вас установлен Docker и Docker Compose. Затем выполните команду:

```bash
docker-compose up --build
```

### 4. Проверьте доступность API
API будет доступно по адресу: [http://localhost:8000](http://localhost:8000).

- **Получить последнюю запись**: `GET /last-record`
- **Получить все записи**: `GET /all-records`

### 5. Тестирование обработки видео
Для обработки видео добавьте файл `test_video.mp4` в корневую директорию или настройте источник камеры в переменной `VIDEO_SOURCE` в `main.py`.

### 6. Инициализация базы данных
Скрипт `init.sql` автоматически создаёт таблицу `vehicle_numbers` в базе данных PostgreSQL.


## 📋 Возможности

1. Распознавание автомобильных номерных знаков из видео или с камеры.
2. Сохранение данных (номер, изображение, временная метка) в PostgreSQL.
3. REST API для взаимодействия с данными.




Проект распространяется под лицензией MIT. См. [LICENSE](LICENSE) для подробностей.

---

Если нужно что-то добавить или изменить, сообщите!
