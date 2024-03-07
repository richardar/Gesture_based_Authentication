from deepface import DeepFace


import cv2

cap = cv2.VideoCapture(0)

while(cap.isOpened()):
    success, frame = cap.read()
    if not success:
        continue
    
    dfs = DeepFace.find(img_path=frame, db_path=r"C:\Users\gratu\Projects\Gesture_Based_Authentication\facedatabase")
    print(dfs)
    cv2.imshow('frame',frame)