from __future__ import annotations

from flask import Flask, jsonify, send_from_directory

from backend.config import FRONTEND_DIST_DIR, STATIC_ASSETS_DIR
from backend.routes.api import api_bp
from backend.services.runtime import start_background_traffic, stop_background_traffic

app = Flask(__name__, static_folder=None)
app.register_blueprint(api_bp)


def _frontend_ready() -> bool:
    return FRONTEND_DIST_DIR.exists() and (FRONTEND_DIST_DIR / "index.html").exists()


@app.before_request
def ensure_background_traffic():
    start_background_traffic()


@app.get("/assets/<path:filename>")
def frontend_assets(filename: str):
    if STATIC_ASSETS_DIR.exists():
        return send_from_directory(STATIC_ASSETS_DIR, filename)
    return jsonify({"error": "Frontend assets not built yet."}), 404


@app.get("/")
@app.get("/<path:path>")
def frontend(path: str = ""):
    requested_path = FRONTEND_DIST_DIR / path
    if path and requested_path.exists() and requested_path.is_file():
        return send_from_directory(FRONTEND_DIST_DIR, path)

    if _frontend_ready():
        return send_from_directory(FRONTEND_DIST_DIR, "index.html")

    return jsonify(
        {
            "message": "Frontend build not found. Run the React frontend build first.",
            "recommended_steps": [
                "npm install",
                "npm run build",
                "python app.py",
            ],
        }
    ), 503


if __name__ == "__main__":
    start_background_traffic()
    app.run(debug=False, host="0.0.0.0", port=5000, threaded=True)
