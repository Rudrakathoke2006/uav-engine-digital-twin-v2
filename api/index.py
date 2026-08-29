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

from app.main import app as fastapi_app

class VercelPathFixMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope.get("type") == "http":
            headers = dict(scope.get("headers", []))
            matched_path = headers.get(b"x-matched-path", b"").decode("utf-8")
            forwarded_uri = headers.get(b"x-forwarded-uri", b"").decode("utf-8")
            
            req_path = matched_path or forwarded_uri or scope.get("path", "")
            if req_path and req_path not in ("/api/index.py", "/api/index", "/api/index.py/", "/api/index/"):
                scope["path"] = req_path
            else:
                scope["path"] = "/"
        await self.app(scope, receive, send)

app = VercelPathFixMiddleware(fastapi_app)


