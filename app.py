from backend.app import app, start_background_traffic, stop_background_traffic

__all__ = ["app", "start_background_traffic", "stop_background_traffic"]


if __name__ == "__main__":
    start_background_traffic()
    app.run(debug=False, host="0.0.0.0", port=5000, threaded=True)
