import cv2
from collections import deque
from datetime import datetime
import os
from dotenv import load_dotenv
from nomeroff_processor import process_image
from postgres_client import PostgresConnection

load_dotenv()

NUMBER_BUFFER_SIZE = 5


def process_video(video_source, is_camera=False):
    """
    Обрабатывает видео с камеры или файла, сохраняет данные в PostgreSQL при выполнении условий.
    
    :param video_source: Путь к видеофайлу или индекс камеры.
    :param is_camera: Указывает, используется ли камера.
    """
    postgres_client = PostgresConnection.get_instance()
    
    number_buffer = deque(maxlen=NUMBER_BUFFER_SIZE)
    
    video_capture = cv2.VideoCapture(video_source)
    
    if not video_capture.isOpened():
        raise ValueError(f"Не удалось открыть видеоисточник: {video_source}")
    
    while True:
        ret, frame = video_capture.read()
        
        if not ret:
            if is_camera:
                continue  
            else:
                break  
        
        temp_image_path = "temp_frame.jpg"
        cv2.imwrite(temp_image_path, frame)
        
        _, detected_number, timestamp = process_image(temp_image_path)
        
        os.remove(temp_image_path)
        
        if detected_number:
            number_buffer.append(detected_number)
            print(f"Обнаруженный номер: {detected_number}")
        
            if len(number_buffer) == NUMBER_BUFFER_SIZE and len(set(number_buffer)) == 1:
                save_to_postgres(postgres_client, frame, detected_number, timestamp)
                number_buffer.clear()  
            
        if not is_camera:
            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    video_capture.release()
    cv2.destroyAllWindows()


def save_to_postgres(postgres_client, frame, number, timestamp):
    """
    Сохраняет кадр, номер и таймстамп в PostgreSQL.
    
    :param postgres_client: Объект подключения к PostgreSQL.
    :param frame: Кадр в формате numpy array.
    :param number: Обнаруженный номерной знак.
    :param timestamp: Временная метка.
    """
    _, buffer = cv2.imencode('.jpg', frame)
    image_data = buffer.tobytes()
    
    table_name = "vehicle_numbers"
    data = {
        "number": number,
        "timestamp": timestamp.isoformat(),
        "image": image_data
    }
    
    postgres_client.set_data_to_postgres(table_name, key=number, value=data)
    print(f"Данные записаны: {number}, {timestamp}")


if __name__ == "__main__":
    ENV = os.getenv("ENV", "dev")
    VIDEO_SOURCE = 0 if ENV == "prod" else "test_video.mp4"  
    IS_CAMERA = ENV == "prod"
    
    process_video(VIDEO_SOURCE, is_camera=IS_CAMERA)
