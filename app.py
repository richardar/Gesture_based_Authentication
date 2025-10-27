try:
    import cv2
    CV2_AVAILABLE = True
except Exception:
    CV2_AVAILABLE = False

import os
try:
    import pyttsx3
    speech_engine = pyttsx3.init()
    speech_engine.setProperty('rate', 150)
except Exception:
    class _DummySpeech:
        def say(self, text):
            print('[TTS]', text)

        def runAndWait(self):
            pass

    speech_engine = _DummySpeech()

from facerecognition import recognize
from gesturerecognitiontask import Authentication_task


def run_auth(device=0):

    # try to import heavier models optionally
    use_yolo = False
    try:
        from ultralytics import YOLO
        model = YOLO(os.path.join(os.getcwd(), 'yolov8n.pt'))
        use_yolo = True
    except Exception:
        model = None

    if not CV2_AVAILABLE:
        print('Error: OpenCV (cv2) is not installed. Install opencv-python to run the app.')
        return

    # camera
    cap = cv2.VideoCapture(device)
    try:
        if not cap.isOpened():
            print('Cannot open camera')
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            # If YOLO available try person detection to focus the face
            cropped = None
            if use_yolo and model is not None:
                try:
                    persons = model.predict(frame, classes=[0], verbose=False, conf=0.6)
                    if persons and len(persons[0].boxes.xyxy) >= 1:
                        # take the first person box
                        x1, y1, x2, y2 = map(int, persons[0].boxes.xyxy[0])
                        cropped = frame[max(0, y1):y2, max(0, x1):x2]
                except Exception:
                    cropped = None

            # fallback: use entire frame
            if cropped is None:
                cropped = frame

            # perform face recognition
            fr = recognize('facedatabase', cropped)

            if fr == 2:
                print('Could not detect a face — please show your full face to the camera')
                speech_engine.say('Show your full face to the camera')
                speech_engine.runAndWait()
                continue

            if not fr:
                print('Face not recognized — not authorized')
                speech_engine.say('Face not recognized, please try again')
                speech_engine.runAndWait()
                continue

            # recognized
            print(f'Successfully recognized: {fr}')
            speech_engine.say(f'Welcome {fr}. Now show the gesture sequence')
            speech_engine.runAndWait()

            auth_ok = Authentication_task()
            if auth_ok:
                print('Authentication succeeded')
                speech_engine.say('Authentication succeeded. Access granted')
                speech_engine.runAndWait()
                break
            else:
                print('Gesture authentication failed — restarting')
                speech_engine.say('Gesture authentication failed. Try again')
                speech_engine.runAndWait()

    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    run_auth()

