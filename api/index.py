import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
backend_dir = os.path.join(root_dir, "uav-engine-digital-twin", "backend")

if root_dir not in sys.path:
    sys.path.append(root_dir)

if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.main import app
