"""Minimal Flask web UI to test face and gesture inputs via file upload.

Provides endpoints:
- GET /          : simple HTML form
- POST /analyze  : accept an image file and run face & gesture recognition

This avoids requiring a camera in the web UI and is useful for testing.
"""
from flask import Flask, request, jsonify, render_template_string
from io import BytesIO
from PIL import Image
import os

import facerecognition
import gesturerecognition


app = Flask(__name__)

INDEX_HTML = '''
<!doctype html>
<title>Gesture Auth UI</title>
<h1>Upload an image to analyze</h1>
<form action="/analyze" method=post enctype=multipart/form-data>
  <input type=file name=file>
  <input type=submit value=Upload>
</form>
'''


@app.route('/')
def index():
    return render_template_string(INDEX_HTML)


@app.route('/analyze', methods=['POST'])
def analyze():
    f = request.files.get('file')
    if not f:
        return jsonify({'error': 'no file provided'}), 400

    img = Image.open(BytesIO(f.read())).convert('RGB')
    # write a temporary file to allow existing helpers to accept path or numpy
    tmp_path = os.path.join(os.getcwd(), 'tmp_upload.jpg')
    img.save(tmp_path)

    # face recognition: use the saved file path (facerecognition supports path)
    fr = facerecognition.recognize('facedatabase', tmp_path)

    # gesture recognition: convert PIL image to numpy BGR without cv2
    import numpy as np
    arr = np.array(img)  # RGB
    # convert RGB->BGR for existing helpers that expect BGR
    bgr = arr[:, :, ::-1]
    gesture = gesturerecognition.gesturerecog(bgr)

    return jsonify({'face': fr, 'gesture': gesture})


def run_server(host='0.0.0.0', port=5000):
    app.run(host=host, port=port)


if __name__ == '__main__':
    run_server()
