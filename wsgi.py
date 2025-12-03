"""App entry point."""
import os
import atexit
from filters import create_app

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

def cleanup_uploads():
    try:
        if os.path.exists(UPLOAD_FOLDER):
            for fname in os.listdir(UPLOAD_FOLDER):
                try:
                    os.remove(os.path.join(UPLOAD_FOLDER, fname))
                except Exception:
                    pass
    except Exception:
        pass

atexit.register(cleanup_uploads)

app = create_app()

if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=5000, debug=debug, use_reloader=debug)