import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

modules = ['app', 'facerecognition', 'gesturerecognition', 'gesturerecognitiontask']
import importlib

for m in modules:
    try:
        importlib.import_module(m)
        print('OK', m)
    except Exception as e:
        print('ERR', m, ':', e)
