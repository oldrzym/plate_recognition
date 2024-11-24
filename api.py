from fastapi import FastAPI, HTTPException
from psycopg2.extras import RealDictCursor
from postgres_client import PostgresConnection

app = FastAPI()

postgres_client = PostgresConnection.get_instance()

@app.get("/last-record")
def get_last_record():
    """
    Получить последнюю запись из таблицы `vehicle_numbers`.
    """
    try:
        with postgres_client.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM vehicle_numbers ORDER BY id DESC LIMIT 1;")
            record = cursor.fetchone()
            if not record:
                raise HTTPException(status_code=404, detail="Последняя запись не найдена.")
            return record
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при запросе: {e}")


@app.get("/all-records")
def get_all_records():
    """
    Получить все записи из таблицы `vehicle_numbers`.
    """
    try:
        with postgres_client.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM vehicle_numbers;")
            records = cursor.fetchall()
            if not records:
                raise HTTPException(status_code=404, detail="Записи в таблице не найдены.")
            return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при запросе: {e}")
