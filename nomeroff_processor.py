import cv2
from datetime import datetime
from nomeroff_net import pipeline
from nomeroff_net.tools import unzip

def process_image(image_path):
    """
    Обрабатывает изображение, извлекает номерной знак и возвращает исходное изображение, номерной знак и таймстамп.
    
    :param image_path: Путь к изображению.
    :return: Исходное изображение, распознанный номерной знак, текущий таймстамп.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Изображение не найдено по пути: {image_path}")

    number_plate_detection_and_reading = pipeline("number_plate_detection_and_reading", image_loader="opencv")

    (images, images_bboxs, images_points, images_zones, region_ids, 
     region_names, count_lines, confidences, texts) = unzip(
        number_plate_detection_and_reading([image_path])
    )
    
    if not texts:
        return image, None, datetime.now()

    detected_number = texts[0]  
    timestamp = datetime.now()  
    return image, detected_number, timestamp

# if __name__ == "__main__":
#     input_image = "./data/examples/oneline_images/example1.jpeg"  
#     output_image, number_plate, timestamp = process_image(input_image)
    
#     print(f"Номерной знак: {number_plate}")
#     print(f"Таймстамп: {timestamp}")
#     if number_plate:
#         cv2.imshow("Output Image", output_image)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()
