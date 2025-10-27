
import os
try:
    import cv2
    CV2_AVAILABLE = True
except Exception:
    CV2_AVAILABLE = False
try:
    # prefer mediapipe tasks if installed
    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision
    MP_TASKS_AVAILABLE = True
except Exception:
    MP_TASKS_AVAILABLE = False

try:
    import mediapipe as mp
    MP_AVAILABLE = True
except Exception:
    MP_AVAILABLE = False

from PIL import Image
import tempfile


def _thumb_up_from_hands(image_bgr):

    if not MP_AVAILABLE or not CV2_AVAILABLE:
        return None

    mp_hands = mp.solutions.hands
    with mp_hands.Hands(static_image_mode=True, max_num_hands=1) as hands:
        results = hands.process(cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB))
        if not results.multi_hand_landmarks:
            return None

        lm = results.multi_hand_landmarks[0]
        # landmarks: 4 = thumb_tip, 3 = thumb_ip
        # finger tips: 8 index, 12 middle, 16 ring, 20 pinky
        h, w, _ = image_bgr.shape
        def y(idx):
            return lm.landmark[idx].y * h

        # thumb extended upwards: thumb tip is above (smaller y) than thumb ip
        thumb_extended = y(4) < y(3)

        # other fingers folded: tip below pip (y_tip > y_pip)
        folded = True
        finger_tips = [(8, 6), (12, 10), (16, 14), (20, 18)]
        for tip, pip in finger_tips:
            if y(tip) < y(pip) - 5:  # tip above pip -> finger extended
                folded = False
                break

        if thumb_extended and folded:
            return 'Thumb_Up'
        return None


def gesturerecog(image_bgr):

    # first try mediapipe tasks & model file
    model_path = os.path.join(os.getcwd(), 'gesture_recognizer.task')
    if MP_TASKS_AVAILABLE and os.path.exists(model_path) and CV2_AVAILABLE:
        # convert to RGB PIL image and write to temp file for the tasks API
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(image_rgb)
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.GestureRecognizerOptions(base_options=base_options)
        recognizer = vision.GestureRecognizer.create_from_options(options)

        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
            pil_img.save(f.name)
            temp_path = f.name

        try:
            mp_image = mp.Image.create_from_file(temp_path)
            res = recognizer.recognize(mp_image)
            if not res or len(res.gestures) == 0:
                return None
            first = res.gestures[0]
            if not first:
                return None
            name = first[0].category_name
            if name == 'None':
                return None
            return name
        except Exception:
            return None
        finally:
            try:
                os.remove(temp_path)
            except Exception:
                pass

    # fallback to MediaPipe Hands heuristic
    try:
        return _thumb_up_from_hands(image_bgr)
    except Exception:
        return None


