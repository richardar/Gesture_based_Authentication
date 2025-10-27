try:
    import cv2
    CV2_AVAILABLE = True
except Exception:
    CV2_AVAILABLE = False

try:
    import pyttsx3
    speech_engine = pyttsx3.init()
    speech_engine.setProperty('rate', 150)
except Exception:
    # lightweight fallback if pyttsx3 is not available
    class _DummySpeech:
        def say(self, text):
            print('[TTS]', text)

        def runAndWait(self):
            pass

    speech_engine = _DummySpeech()

from gesturerecognition import gesturerecog

# expected gesture sequence for authentication
Authentication_gesture = ['Thumb_Up', 'Thumb_Up', 'Thumb_Up']


def capture_image(device=0):
    """Capture a single frame from the camera and return the BGR image."""
    cap = cv2.VideoCapture(device)
    try:
        if not cap.isOpened():
            print("Error: Unable to access the camera")
            return None

        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture image")
            return None

        # small local file for debugging/optional use
        cv2.imwrite("captured_image.jpg", frame)
        speech_engine.say("Captured image")
        speech_engine.runAndWait()
        return frame
    finally:
        cap.release()


def Authentication_task(retries=10):

    captured_gesture = []

    for i in range(retries):
        # Prompt the user before capture
        speech_engine.say(f"Show gesture number {i+1} in five seconds")
        speech_engine.runAndWait()

        frame = capture_image()
        if frame is None:
            continue

        gesture = gesturerecog(frame)

        if gesture is None:
            # no gesture detected for this attempt
            continue

        # record only expected gestures
        if gesture == Authentication_gesture[len(captured_gesture)]:
            captured_gesture.append(gesture)
            # check if we have the full sequence
            if len(captured_gesture) == len(Authentication_gesture):
                # exact match
                return True
        else:
            # mismatch — reset sequence and allow retries
            captured_gesture = []

    return False

