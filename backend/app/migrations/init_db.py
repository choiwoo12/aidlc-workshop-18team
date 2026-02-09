"""
Database Initialization Script
"""
from app.utils.database import init_db, SessionLocal
from app.models.store import Store
from app.models.table import Table, TableStatus
from app.utils.auth import hash_password


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
            name="Test Store",
            admin_username="admin",
            admin_password_hash=hash_password("admin1234")
        )
        db.add(store)
        db.commit()
        db.refresh(store)
        
        print("Initial data created successfully:")
        print(f"  Store: {store.name}")
        print(f"  Admin Username: {store.admin_username}")
        print(f"  Admin Password: admin1234")
        
        # Create initial tables (1-10)
        print("\nCreating tables...")
        for i in range(1, 11):
            table = Table(
                store_id=store.id,
                table_number=str(i),
                status=TableStatus.AVAILABLE,
                capacity=4
            )
            db.add(table)
        
        db.commit()
        print(f"  Created 10 tables (1-10)")
        
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
