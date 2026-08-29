import sys
import os

# Calculate absolute paths
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
backend_dir = os.path.join(root_dir, "uav-engine-digital-twin", "backend")

# Remove root_dir from sys.path so root app.py does not shadow the backend/app package
sys.path = [p for p in sys.path if os.path.abspath(p) != os.path.abspath(root_dir)]
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.main import app
