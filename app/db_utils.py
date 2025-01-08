from app.database import init_db, close_db

def setup_database():
    print("Setting up database...")
    init_db()

def teardown_database():
    print("Tearing down database...")
    close_db()
