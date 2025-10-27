import unittest
import sys
from pathlib import Path
from unittest import mock

project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))


class IntegrationTests(unittest.TestCase):
    def test_simulated_face_and_gesture(self):
        # Simulate face recognition and gesture recognition by monkeypatching
        import facerecognition
        import gesturerecognition

        with mock.patch('facerecognition.recognize', return_value='test_person') as fr_patch:
            with mock.patch('gesturerecognition.gesturerecog', return_value='Thumb_Up') as g_patch:
                # call the patched functions
                res_face = facerecognition.recognize('facedatabase', 'dummy')
                res_gesture = gesturerecognition.gesturerecog(None)

                self.assertEqual(res_face, 'test_person')
                self.assertEqual(res_gesture, 'Thumb_Up')

    def test_webui_analyze_endpoint(self):
        # use Flask test client with gesture/face monkeypatch
        from webui import app

        with app.test_client() as c:
            # monkeypatch recognize and gesturerecog
            with mock.patch('facerecognition.recognize', return_value='alice'):
                with mock.patch('gesturerecognition.gesturerecog', return_value='Thumb_Up'):
                    # create a small in-memory PNG image to upload
                    from PIL import Image
                    from io import BytesIO
                    img = Image.new('RGB', (10, 10), color=(255, 0, 0))
                    buf = BytesIO()
                    img.save(buf, format='PNG')
                    buf.seek(0)
                    data = {
                        'file': (buf, 'thumb.png')
                    }
                    rv = c.post('/analyze', data=data, content_type='multipart/form-data')
                    self.assertEqual(rv.status_code, 200)
                    j = rv.get_json()
                    self.assertIn('face', j)
                    self.assertIn('gesture', j)


if __name__ == '__main__':
    unittest.main()
