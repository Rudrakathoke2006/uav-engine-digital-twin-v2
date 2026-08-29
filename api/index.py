import sys
import os

# Add backend directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'uav-engine-digital-twin', 'backend'))

try:
    from app.main import app
except ImportError:
    from uav_engine_digital_twin.backend.app.main import app
