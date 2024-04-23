import math
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os
from PIL import Image
from io import BytesIO
import tempfile

def gesturerecog(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    image = Image.fromarray(image)
    base_options = python.BaseOptions(model_asset_path=os.path.join(os.getcwd(),"gesture_recognizer.task"))
    print('done loading model :)')
    options = vision.GestureRecognizerOptions(base_options=base_options)
    recognizer = vision.GestureRecognizer.create_from_options(options)
    
    # Convert PIL image to a temporary file
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
        image.save(temp_file.name)
        temp_file_path = temp_file.name

    try:
        # Create mp.Image from file path
        mp_image = mp.Image.create_from_file(temp_file_path)

        # Recognize gestures in the input image
        recognition_result = recognizer.recognize(mp_image)
        if recognition_result == [] :
            return None
        if recognition_result.gestures[0][0].category_name == "None":
            return None
        print(recognition_result.gestures[0][0].category_name)
        return recognition_result.gestures[0][0].category_name

    finally:
        # Clean up: Remove the temporary file
        os.remove(temp_file_path)

# Example usage:


# if __name__ == "__main__":
#     image_path = r"C:\Users\gratu\Projects\Gesture_Based_Authentication\_d39098cf-7c7d-48e6-9c8a-eb605e5a40d2.jpeg"
#     pil_image = Image.open(image_path)
#     facerecog(pil_image)

