import cv2
from ultralytics import YOLO
from retinaface import RetinaFace
from facerecognition import recognize
import pyttsx3
import os
from gesturerecognition import gesturerecog

os.environ['KMP_DUPLICATE_LIB_OK']='True'

# Initialize YOLO model
model = YOLO('yolov8n.pt')

# Initialize text to speech
speech_engine = pyttsx3.init()
speech_engine.setProperty('rate', 150)

# Open camera
cap = cv2.VideoCapture(0)

while cap.isOpened():
    # Read frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to read frame")
        continue
    
    # Perform person detection
    persons = model.predict(frame, classes=[0], show=False, verbose=False, conf=0.7)
    
    # Check number of persons detected
    if len(persons[0].boxes.xyxy) == 1:
        speech_engine.say("Person detected, moving on with face recognition")
        speech_engine.runAndWait()
        
        # Extract person's face
        person_box = persons[0].boxes.xyxy[0]
        person_xmin, person_ymin, person_xmax, person_ymax = map(int, person_box)
        cropped_person = frame[person_ymin:person_ymax, person_xmin:person_xmax]

        # Perform face recognition
        fr = recognize("facedatabase", cropped_person)

        if not fr:
            speech_engine.say("Failed to recognize your face, you are not authorized")
            speech_engine.runAndWait()
            print("Failed to recognize your face, you are not authorized, trying again")
        elif fr == 2:
            print("Show your complete face to recognizer for it to work properly")
        else:
            print("Successfully recognized your face {}".format(fr))
            speech_engine.say("Successfully recognized. Welcome {}, now let's move on to showing gestures".format(fr))
            speech_engine.runAndWait()
            # speech_engine.say("Now sir, show your first gesture in 5, 4, 3, 2, 1")
            # speech_engine.runAndWait()

            # # Perform gesture recognition
            # gesture_cap = cv2.VideoCapture(0)
            # while gesture_cap.isOpened():
            #     ret, gesture = gesture_cap.read()
            #     if ret:
            #         cv2.imshow("Gesture", gesture)
            #         gesturerecog(gesture)
            #     # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     #     break

            # gesture_cap.release()
            
    elif len(persons[0].boxes.xyxy) > 1:
        print("Cannot have more than one person on the frame")
    else:
        continue

    # cv2.imshow('Frame', frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

cap.release()
cv2.destroyAllWindows()
