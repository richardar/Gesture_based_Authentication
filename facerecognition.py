

import os
import numpy as np

try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except Exception:
    DEEPFACE_AVAILABLE = False

try:
    import face_recognition
    FACE_RECOG_AVAILABLE = True
except Exception:
    FACE_RECOG_AVAILABLE = False


def _is_image_file(name):
    return name.lower().endswith(('.jpeg', '.png', '.jpg'))


def recognize(database, imagetofind):

    try:
        folders = [f for f in os.listdir(database) if os.path.isdir(os.path.join(database, f))]

        # If DeepFace is available, prefer it (simpler API)
        if DEEPFACE_AVAILABLE:
            for folder in folders:
                person_dir = os.path.join(database, folder)
                for fname in os.listdir(person_dir):
                    if not _is_image_file(fname):
                        continue
                    try:
                        img2 = os.path.join(person_dir, fname)
                        resp = DeepFace.verify(imagetofind, img2, enforce_detection=False)
                        if isinstance(resp, dict) and resp.get('verified'):
                            return folder
                    except Exception:
                        continue

            return 0

        # Fallback to face_recognition
        if FACE_RECOG_AVAILABLE:
            # compute encoding of input image
            if isinstance(imagetofind, str):
                unknown_img = face_recognition.load_image_file(imagetofind)
            else:
                # assume numpy BGR (OpenCV) -> convert to RGB
                unknown_img = imagetofind[:, :, ::-1]

            unknown_encs = face_recognition.face_encodings(unknown_img)
            if not unknown_encs:
                return 2  # no face found
            unknown_enc = unknown_encs[0]

            for folder in folders:
                person_dir = os.path.join(database, folder)
                for fname in os.listdir(person_dir):
                    if not _is_image_file(fname):
                        continue
                    try:
                        cand = face_recognition.load_image_file(os.path.join(person_dir, fname))
                        encs = face_recognition.face_encodings(cand)
                        if not encs:
                            continue
                        match = face_recognition.compare_faces([encs[0]], unknown_enc, tolerance=0.6)
                        if match[0]:
                            return folder
                    except Exception:
                        continue

            return 0

        # If neither library is available raise an informative error
        print('Error: No face recognition backend available (install deepface or face_recognition)')
        return 2

    except Exception as e:
        print('Face recognition error:', e)
        return 2
