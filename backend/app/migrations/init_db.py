"""
Database Initialization Script
"""
from backend.app.utils.database import init_db, SessionLocal
from backend.app.models.store import Store
from backend.app.utils.auth import hash_password


def create_initial_data():
    """
    Create initial data for testing
    """
    db = SessionLocal()
    
    try:
        # Check if store already exists
        existing_store = db.query(Store).first()
        if existing_store:
            print("Store already exists. Skipping initial data creation.")
            return
        
        # Create initial store with admin account
        store = Store(
            name="테스트 매장",
            admin_username="admin",
            admin_password_hash=hash_password("admin1234")
        )
        db.add(store)
        db.commit()
        
        print("Initial data created successfully:")
        print(f"  Store: {store.name}")
        print(f"  Admin Username: {store.admin_username}")
        print(f"  Admin Password: admin1234")
        
    except Exception as e:
        print(f"Error creating initial data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialized.")
    
    print("\nCreating initial data...")
    create_initial_data()
    print("Done.")
