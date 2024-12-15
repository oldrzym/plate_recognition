import os
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class PostgresConnection:
    __instance = None

    def __init__(self, host, port, user, password, database):
        self.connection = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        self.connection.autocommit = True
        print("Connected to PostgreSQL")

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls(
                os.getenv("POSTGRES_HOST_SERVICE", "localhost"),
                int(os.getenv("POSTGRES_PORT", 5432)),
                os.getenv("POSTGRES_USER", "user"),
                os.getenv("POSTGRES_PASSWORD", "password"),
                os.getenv("POSTGRES_DB", "app_db")
            )
        return cls.__instance

    def save_record(self, number: str, timestamp: datetime, image: bytes):
        with self.connection.cursor() as cursor:
            query = sql.SQL("""
                INSERT INTO vehicle_numbers (number, timestamp, image) 
                VALUES (%s, %s, %s)
            """)
            cursor.execute(query, (number, timestamp.isoformat(), image))

    def get_last_record(self):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM vehicle_numbers ORDER BY id DESC LIMIT 1;")
            return cursor.fetchone()

    def get_all_records(self):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM vehicle_numbers;")
            return cursor.fetchall()

    def get_records_by_date(self, start: datetime, end: datetime):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            query = """
                SELECT * FROM vehicle_numbers 
                WHERE timestamp >= %s AND timestamp <= %s
                ORDER BY timestamp ASC;
            """
            cursor.execute(query, (start, end))
            return cursor.fetchall()
