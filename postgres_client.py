import os
import psycopg2
from psycopg2 import sql
from psycopg2.extras import Json
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()


class KeyNotFound(Exception):
    pass


class PostgresConnection:
    __instance = None

    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        try:
            self.connection = psycopg2.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            self.connection.autocommit = True
            print("Соединение с PostgreSQL установлено успешно.")
        except psycopg2.OperationalError as e:
            print(f"Ошибка подключения к PostgreSQL: {e}")
            raise

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
            cls.__instance.connection = None
        return cls.__instance

    @classmethod
    def get_instance(cls):
        if not cls.__instance or not cls.__instance.connection:
            cls.__instance = cls(
                os.getenv("POSTGRES_HOST", "localhost"),
                int(os.getenv("POSTGRES_PORT", 5432)),
                os.getenv("POSTGRES_USER", "user"),
                os.getenv("POSTGRES_PASSWORD", "password"),
                os.getenv("POSTGRES_DB", "database")
            )
        return cls.__instance

    def get_data_from_postgres(self, table: str, key: str) -> dict:
        with self.connection.cursor() as cursor:
            query = sql.SQL("SELECT data FROM {table} WHERE key = %s").format(table=sql.Identifier(table))
            cursor.execute(query, (key,))
            result = cursor.fetchone()

            if not result:
                raise KeyNotFound(f"Key {key} not found in PostgreSQL")

            return result[0]

    def set_data_to_postgres(self, table: str, data: dict):
        with self.connection.cursor() as cursor:
            query = sql.SQL("""
                INSERT INTO {table} (number, timestamp, image) 
                VALUES (%s, %s, %s)
            """).format(table=sql.Identifier(table))
            cursor.execute(query, (data['number'], data['timestamp'], data['image']))



postgres_client = PostgresConnection.get_instance()
