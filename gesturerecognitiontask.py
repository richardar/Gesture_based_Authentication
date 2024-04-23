import cv2
import pyttsx3
from gesturerecognition import gesturerecog

speech_engine = pyttsx3.init()
speech_engine.setProperty('rate', 150)


Authentication_gesture = ['Thumb_Up','Thumb_Up','Thumb_Up']

import cv2

def capture_image():
    # Initialize the camera
    cap = cv2.VideoCapture(0) 

    if not cap.isOpened():
        print("Error: Unable to access the camera")
        return

    ret, frame = cap.read()

    if ret:
        cv2.imwrite("captured_image.jpg", frame)
        speech_engine.say("captured image successfully ")
        speech_engine.runAndWait()
        
        return frame
    else:
        print("Error: Unable to capture image")

    cap.release()


captured_gesture = []

def Authentication_task():
    for i in range(10):
        
        speech_engine.say("Now sir, show gesture number {} in 5, 4, 3, 2, 1".format(i))
        speech_engine.runAndWait()
        captured_image=capture_image()
        gesture = gesturerecog(captured_image)
        
        if gesture is not None:
            captured_gesture.append(gesture)
            if len(Authentication_gesture) == len(captured_gesture):
                if Authentication_gesture == captured_gesture:
                    return True
            else:
                continue
        else:
            continue
        
    return False
            
