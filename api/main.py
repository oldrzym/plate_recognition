from fastapi import FastAPI, HTTPException, Query
from datetime import datetime
from typing import Optional
from postgres_client import PostgresConnection
import base64
from fastapi.responses import Response
from psycopg2.extras import RealDictCursor

app = FastAPI()

postgres_client = PostgresConnection.get_instance()

def transform_record(record):
    """
    Преобразует запись из PostgreSQL в сериализуемый формат.
    """
    if not record:
        return None
    return {
        "id": record["id"],
        "number": record["number"],
        "timestamp": record["timestamp"].isoformat(),  # Преобразование datetime в строку
        "image": base64.b64encode(record["image"]).decode() if record["image"] else None  # Преобразование BYTEA в base64
    }

@app.get("/last-record")
def get_last_record():
    """
    Получить последнюю запись из таблицы.
    """
    record = postgres_client.get_last_record()
    if not record:
        raise HTTPException(status_code=404, detail="Последняя запись не найдена.")
    return transform_record(record)

@app.get("/all-records")
def get_all_records():
    """
    Получить все записи из таблицы.
    """
    records = postgres_client.get_all_records()
    if not records:
        raise HTTPException(status_code=404, detail="Записи в таблице не найдены.")
    return [transform_record(record) for record in records]

@app.get("/records-by-date")
def get_records_by_date(
    start_date: str = Query(..., description="Начальная дата (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Конечная дата (YYYY-MM-DD)")
):
    """
    Получить записи за указанный период.
    """
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Некорректный формат даты, используйте YYYY-MM-DD.")
    
    records = postgres_client.get_records_by_date(start, end)
    if not records:
        raise HTTPException(status_code=404, detail="Записи за указанный период не найдены.")
    return [transform_record(record) for record in records]

@app.get("/last-record/image")
def get_last_record_image():
    """
    Получить последнюю запись из таблицы `vehicle_numbers` и вернуть изображение.
    """
    try:
        with postgres_client.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT image FROM vehicle_numbers ORDER BY id DESC LIMIT 1;")
            record = cursor.fetchone()
            if not record or not record["image"]:
                raise HTTPException(status_code=404, detail="Запись или изображение не найдены.")
            
            return Response(content=record["image"], media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при извлечении изображения: {e}")