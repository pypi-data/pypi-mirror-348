from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import pathlib

load_dotenv()

# Create app data directory if it doesn't exist
app_data_dir = os.path.join(pathlib.Path.home(), ".finance_news_api")
os.makedirs(app_data_dir, exist_ok=True)

# Get database URL from environment variable or use default SQLite in user home directory
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(app_data_dir, 'users.db')}")

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 