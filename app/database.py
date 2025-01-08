from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os


def get_database_url():
    """Retrieve database connection string from environment variables."""
    return os.getenv("DATABASE_URL", "sqlite:///tasks.db")


Base = declarative_base()
engine = create_engine(get_database_url())
Session = sessionmaker(bind=engine)
db_session = scoped_session(Session)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    def as_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description}

Task.query = db_session.query_property()



def init_db():
    """Initialize the database."""
    from app.database import Base, engine
    Base.metadata.create_all(engine)
    print("Database initialized.")


def close_db():
    """Close the database session."""
    if db_session:
        db_session.remove()
        print("Database session closed.")

