# Gesture_based_Authentication

This repository implements a simple gesture-based authentication prototype.

Features
- Face recognition using DeepFace or a fallback to `face_recognition` if
	# Gesture_based_Authentication

	This repository contains a prototype gesture-based authentication system.
	It combines face recognition with a short gesture sequence to authenticate a
	user. The project is defensive: it uses model-based components when available
	and falls back to lightweight heuristics when optional heavy packages are
	missing so you can run and test it on most machines.

	## Contents
	- `app.py` — camera-based authentication runner
	- `webui.py` — small Flask UI to upload images and test face+gesture analysis
	- `facerecognition.py` — face recognition helpers (DeepFace or `face_recognition` fallback)
	- `gesturerecognition.py` — gesture recognition (MediaPipe Tasks model or a Hands heuristic fallback)
	- `gesturerecognitiontask.py` — capture flow and gesture authentication sequence
	- `cli.py` — convenience CLI: run, web, test
	- `install.ps1` — PowerShell installer (minimal or full with `-Full`)
	- `tests/` — unit + integration tests that run without heavy libs (use monkeypatching)

	## Prerequisites
	- Python 3.8+ recommended (Windows PowerShell examples below). You can use
		a virtualenv or a Conda environment (the repo does not require a specific
		manager).
	- Optional, but recommended for best accuracy:
		- `deepface` or `face_recognition` for face verification
		- `mediapipe` or MediaPipe Tasks (+ `gesture_recognizer.task`) for gesture recognition
		- `ultralytics` and a compatible `torch` for YOLO person detection (`yolov8n.pt` is included)

	Notes about heavy dependencies: the full `requirements.txt` includes many
	packages (DeepFace, PyTorch, TensorFlow, MediaPipe, etc.). Installing the
	full set may be large and take time — use the minimal installer first.

	## Quick setup (Windows PowerShell)

	1. Create a virtual environment and activate it:

	```powershell
	# using venv
	python -m venv .venv
	.\.venv\Scripts\Activate.ps1

	# (or with conda)
	# conda create -n gesture python=3.10 -y; conda activate gesture
	```

	2. Install minimal recommended packages (fast):

	```powershell
	# from project root
	.\install.ps1
	# Activate venv afterwards: .\.venv\Scripts\Activate.ps1
	```

	3. (Optional) Install the full environment (may be large):

	```powershell
	.\install.ps1 -Full
	```

	4. Prepare the face database

	Put labeled images in `facedatabase/<person_name>/` — for example:

	```
	facedatabase/
		alice/
			img1.jpg
			img2.jpg
		bob/
			photo1.png
	```

	The face recognizer will scan each subfolder to find a matching person.

	5. (Optional) Gesture model

	If you have a MediaPipe Tasks gesture model, place it in the repo root as
	`gesture_recognizer.task`. If present (and MediaPipe tasks is installed)
	the project will use that model. Otherwise the code uses a Thumb_Up heuristic
	so the project still runs without the model.

	## Run the project

	Use the CLI for convenience:

	```powershell
	# camera-based authentication (uses webcam)
	python cli.py run

	# start the Flask web UI for uploads (open http://127.0.0.1:5000/)
	python cli.py web

	# run the test-suite (unit + integration)
	python cli.py test
	```

	Or run the app directly:

	```powershell
	python app.py
	```

	### Flask web UI
	The web UI (`webui.py`) accepts image uploads and returns JSON with:
	- `face`: name of recognized person (or 0/2 for not found / error)
	- `gesture`: recognized gesture string (e.g., `Thumb_Up`) or `null`

	This is useful for testing without a webcam.

	## Tests

	There are lightweight tests that do not require the heavy ML dependencies.
	They use monkeypatching to simulate recognition outputs and a Flask test
	client for the web UI.

	Run tests:

	```powershell
	python -m unittest discover -v
	```

	Or run the integration tests only:

	```powershell
	python -m unittest tests.test_integration -v
	```

	## Troubleshooting
	- Error: `No module named 'cv2'` — install `opencv-python` or run `install.ps1`.
	- Error: missing face recognition backend — install `deepface` or `face_recognition`.
	- If the YOLO detector (Ultralytics) fails, the app will fall back to
		running face recognition on the full frame.

	If you see noisy or incorrect face/gesture matches:
	- Add more frontal, well-lit images to `facedatabase/<person>`.
	- Use the model-based gesture flow (`gesture_recognizer.task`) for better
		gesture coverage and accuracy.

	## Advanced / Notes
	- GPU support: if you want to use GPU-accelerated PyTorch for YOLO, install
		a matching `torch` build for your CUDA version before installing
		`ultralytics`.
	- Security: this project is a demo/prototype. Do not rely on it for
		production authentication without additional safeguards (rate-limiting,
		anti-spoofing, secure storage of templates, etc.).

	---

	If you want, I can add a GitHub Actions workflow that runs the tests on push
	and optionally a small demo script that plays back a sample authentication
	video. Tell me which you'd prefer and I'll add it.