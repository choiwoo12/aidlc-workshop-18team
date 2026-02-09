"""
Database Connection Manager
"""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
from app.config import settings
import os

# Create Base class for models
Base = declarative_base()

# Create engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},  # SQLite specific
    poolclass=StaticPool,  # Use static pool for SQLite
    echo=settings.DEBUG,  # Log SQL queries in debug mode
)


# Enable foreign key constraints for SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    """Enable foreign key constraints for SQLite"""
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    """
    Database session dependency for FastAPI
    
    Usage:
        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database
    - Create all tables
    - Create data directory if not exists
    """
    # Create data directory if not exists
    db_dir = os.path.dirname(settings.DB_FILE_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    
    # Import all models to register them with Base
    from app.models import (
        Store, Table, Menu, Order, OrderItem, OrderHistory
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    print(f"Database initialized at: {settings.DB_FILE_PATH}")


def drop_db():
    """
    Drop all tables (for testing purposes)
    """
    Base.metadata.drop_all(bind=engine)
    print("All tables dropped")
