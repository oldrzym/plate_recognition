import os
import cv2
from collections import deque
from dotenv import load_dotenv
from datetime import datetime
from processor import process_frame, process_image
from postgres_client import PostgresConnection

load_dotenv()
ENV = os.getenv("ENV", "dev")
VIDEO_SOURCE = os.getenv("VIDEO_SOURCE", "test_image.jpg")
NUMBER_BUFFER_SIZE = int(os.getenv("NUMBER_BUFFER_SIZE", 3))

try:
    print('1')
    postgres_client = PostgresConnection.get_instance()
except Exception as e:
    print(f"Failed to initialize PostgreSQL connection: {e}")
    exit(1)

def save_to_postgres(number, timestamp, frame):
    try:
        _, buffer = cv2.imencode('.jpg', frame)
        image_data = buffer.tobytes()
        postgres_client.save_record(number, timestamp, image_data)
        print(f"Data saved: {number}, {timestamp}")
    except Exception as e:
        print(f"Error saving data to PostgreSQL: {e}")

if __name__ == "__main__":
    try:
        if ENV == "prod":
            try:
                video_capture = cv2.VideoCapture(VIDEO_SOURCE)

                if not video_capture.isOpened():
                    raise ValueError(f"Cannot open camera at {VIDEO_SOURCE}")
            except Exception as e:
                print(f"Error initializing video capture: {e}")
                exit(1)

            number_buffer = deque(maxlen=NUMBER_BUFFER_SIZE)

            while True:
                try:
                    ret, frame = video_capture.read()
                    if not ret:
                        print("Failed to grab frame, retrying...")
                        continue

                    recognized_text, timestamp, frm = process_frame(frame)
                    if recognized_text:
                        number_buffer.append(recognized_text)
                        print(f"Detected number: {recognized_text}")

                        if len(number_buffer) == NUMBER_BUFFER_SIZE and len(set(number_buffer)) == 1:
                            save_to_postgres(recognized_text, timestamp, frm)
                            number_buffer.clear()
                except Exception as e:
                    print(f"Error processing frame: {e}")

            video_capture.release()
            cv2.destroyAllWindows()
        else:
            test_image_path = "output.jpg"
            try:
                recognized_text, timestamp, frame = process_image(test_image_path)
                if recognized_text:
                    save_to_postgres(recognized_text, timestamp, frame)
            except Exception as e:
                print(f"Error processing test image: {e}")
    except Exception as main_exception:
        print(f"Unhandled exception in main: {main_exception}")
