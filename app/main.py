from flask import Flask
from flask_restx import Api
from app.routes import api as tasks_blueprint
from app.db_utils import setup_database, teardown_database
import signal
from sqlalchemy import select
import threading
import sys

app = Flask(__name__)
api = Api(
    app,
    title="Task Manager API",
    version="1.0",
    description="A simple Task Manager API",
)

api.add_namespace(tasks_blueprint, path="/api")

ready = threading.Event()


@app.route("/health", methods=["GET"])
def health_check():
    """Liveness probe."""
    try:
        from app.database import db_session

        db_session.execute(select(1))
        return {"status": "healthy"}, 200
    except Exception as e:
        print(f"Health check error: {e}")
        return {"status": "unhealthy", "error": str(e)}, 500


@app.route("/readiness", methods=["GET"])
def readiness_check():
    """Readiness probe."""
    if ready.is_set():
        return {"status": "ready"}, 200
    return {"status": "not ready"}, 503


def graceful_shutdown(signum, frame):
    """Handle SIGTERM and SIGINT for graceful shutdown."""
    print("Received signal to terminate. Shutting down gracefully...")
    ready.clear()
    teardown_database()
    print("Cleanup complete. Exiting application.")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, graceful_shutdown)
    signal.signal(signal.SIGINT, graceful_shutdown)

    setup_database()

    ready.set()

    app.run(host="0.0.0.0", port=5000)
