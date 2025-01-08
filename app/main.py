from flask import Flask
from flask_restx import Api
from routes import api as tasks_blueprint
from database import init_db, close_db
import signal
import threading
import sys

app = Flask(__name__)
api = Api(app, title="Task Manager API", version="1.0", description="A simple Task Manager API")

api.add_namespace(tasks_blueprint, path="/api")

ready = threading.Event()

@app.route('/health', methods=['GET'])
def health_check():
    """Liveness probe with DB connectivity check."""
    try:
        from database import db_session
        db_session.execute("SELECT 1")  
        return {"status": "healthy", "database": "connected"}, 200
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}, 500


@app.route('/readiness', methods=['GET'])
def readiness_check():
    """Readiness probe."""
    if ready.is_set():
        return {"status": "ready"}, 200
    return {"status": "not ready"}, 503

def graceful_shutdown(signum, frame):
    """Handle SIGTERM and SIGINT for graceful shutdown."""
    print("Received signal to terminate. Shutting down gracefully...")
    ready.clear()
    close_db()
    print("Cleanup complete. Exiting application.")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, graceful_shutdown)
    signal.signal(signal.SIGINT, graceful_shutdown)

    init_db()

    ready.set()

    app.run(host="0.0.0.0", port=5000)
