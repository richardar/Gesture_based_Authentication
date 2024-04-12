import cv2
from ultralytics import YOLO
from retinaface import RetinaFace
from facerecognition import  recognize
import pyttsx3
import os
cap = cv2.VideoCapture(0)
model = YOLO('yolov8n.pt')
import os

os.environ['KMP_DUPLICATE_LIB_OK']='True'
#initialize text to speech    
speech_engine = pyttsx3.init()
speech_engine.setProperty('rate',150)

while cap.isOpened():

    suc,frame = cap.read()

    if not suc:
        print("failed to read frame")
        continue
    else:
        persons = model.predict(frame,classes =[0],show=False,verbose=False)
        print(persons[0].boxes.xyxy)

        if len(persons[0].boxes.xyxy) >=2:
            print("cannnot have more than one person on the frame ")
        

        elif len(persons[0].boxes.xyxy) == 1:
            speech_engine.say("person detected, moving on with face recognition")
            speech_engine.runAndWait()
            print("person detected, moving on with face recognition")
            personxmin,personymin,personxmax,personymax = map(int,persons[0].boxes.xyxy[0])
            croppedperson = frame.copy()
            croppedperson = croppedperson[personymin:personymax,personxmin:personxmax]
            cv2.imshow('frame',croppedperson)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


             
            fr = recognize(r"C:\Users\gratu\Projects\Gesture_Based_Authentication\facedatabase",croppedperson)
            print(fr)

            if not fr:
                speech_engine.say("failed to recognize your face, you are not authorized")
                speech_engine.runAndWait()
                print("failed to recognize your face, you re probably not authorized, trying again")
            elif fr == 2:
                print("show your complete face to recognizer for it to work properly")


            else:
                print('successfully recognized your face {}'.format(fr))
                speech_engine.say("successfully recognized. Welcome  {} ,  now let's move on to showing gestures ".format(fr))
                speech_engine.runAndWait()


                
        else:
            continue
                

    

        