"""
Database Initialization Script
"""
from app.utils.database import init_db, SessionLocal
from app.models.store import Store
from app.models.table import Table, TableStatus
from app.models.menu import Menu
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
                status=TableStatus.AVAILABLE
            )
            db.add(table)
        
        db.commit()
        print(f"  Created 10 tables (1-10)")
        
        # Create sample menus
        print("\nCreating sample menus...")
        sample_menus = [
            # Main Dishes
            {
                "name": "Margherita Pizza",
                "description": "Classic pizza with tomato sauce, mozzarella, and basil",
                "price": 12000,
                "category_level1": "Main",
                "category_level2": "Pizza",
                "is_available": True,
                "options": [
                    {"name": "Extra Cheese", "price": 2000},
                    {"name": "Extra Basil", "price": 1000}
                ]
            },
            {
                "name": "Pepperoni Pizza",
                "description": "Pizza with tomato sauce, mozzarella, and pepperoni",
                "price": 14000,
                "category_level1": "Main",
                "category_level2": "Pizza",
                "is_available": True,
                "options": [
                    {"name": "Extra Cheese", "price": 2000},
                    {"name": "Extra Pepperoni", "price": 3000}
                ]
            },
            {
                "name": "Spaghetti Carbonara",
                "description": "Creamy pasta with bacon and parmesan",
                "price": 13000,
                "category_level1": "Main",
                "category_level2": "Pasta",
                "is_available": True,
                "options": [
                    {"name": "Extra Bacon", "price": 2000},
                    {"name": "Extra Parmesan", "price": 1000}
                ]
            },
            {
                "name": "Beef Burger",
                "description": "Juicy beef patty with lettuce, tomato, and cheese",
                "price": 11000,
                "category_level1": "Main",
                "category_level2": "Burger",
                "is_available": True,
                "options": [
                    {"name": "Extra Patty", "price": 3000},
                    {"name": "Bacon", "price": 2000},
                    {"name": "Avocado", "price": 2000}
                ]
            },
            # Appetizers
            {
                "name": "Caesar Salad",
                "description": "Fresh romaine lettuce with caesar dressing",
                "price": 8000,
                "category_level1": "Appetizer",
                "category_level2": "Salad",
                "is_available": True,
                "options": [
                    {"name": "Grilled Chicken", "price": 3000},
                    {"name": "Extra Dressing", "price": 500}
                ]
            },
            {
                "name": "French Fries",
                "description": "Crispy golden fries",
                "price": 5000,
                "category_level1": "Appetizer",
                "category_level2": "Sides",
                "is_available": True,
                "options": [
                    {"name": "Cheese Sauce", "price": 1000},
                    {"name": "Truffle Oil", "price": 2000}
                ]
            },
            {
                "name": "Chicken Wings",
                "description": "Spicy buffalo wings with ranch dip",
                "price": 9000,
                "category_level1": "Appetizer",
                "category_level2": "Chicken",
                "is_available": True,
                "options": [
                    {"name": "Extra Spicy", "price": 0},
                    {"name": "BBQ Sauce", "price": 500}
                ]
            },
            # Beverages
            {
                "name": "Coca Cola",
                "description": "Classic cola drink",
                "price": 3000,
                "category_level1": "Beverage",
                "category_level2": "Soft Drink",
                "is_available": True,
                "options": []
            },
            {
                "name": "Orange Juice",
                "description": "Freshly squeezed orange juice",
                "price": 4000,
                "category_level1": "Beverage",
                "category_level2": "Juice",
                "is_available": True,
                "options": []
            },
            {
                "name": "Iced Americano",
                "description": "Cold espresso with water",
                "price": 4500,
                "category_level1": "Beverage",
                "category_level2": "Coffee",
                "is_available": True,
                "options": [
                    {"name": "Extra Shot", "price": 500},
                    {"name": "Vanilla Syrup", "price": 500}
                ]
            },
            # Desserts
            {
                "name": "Chocolate Cake",
                "description": "Rich chocolate cake with ganache",
                "price": 7000,
                "category_level1": "Dessert",
                "category_level2": "Cake",
                "is_available": True,
                "options": [
                    {"name": "Ice Cream", "price": 2000},
                    {"name": "Whipped Cream", "price": 1000}
                ]
            },
            {
                "name": "Tiramisu",
                "description": "Italian coffee-flavored dessert",
                "price": 8000,
                "category_level1": "Dessert",
                "category_level2": "Cake",
                "is_available": True,
                "options": []
            }
        ]
        
        for menu_data in sample_menus:
            menu = Menu(
                store_id=store.id,
                name=menu_data["name"],
                description=menu_data["description"],
                price=menu_data["price"],
                category_level1=menu_data["category_level1"],
                category_level2=menu_data["category_level2"],
                is_available=menu_data["is_available"],
                options=menu_data["options"]
            )
            db.add(menu)
        
        db.commit()
        print(f"  Created {len(sample_menus)} sample menus")
        
    except Exception as e:
        print(f"Error creating initial data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialized.")
    
    print("\nCreating initial data...")
    create_initial_data()
    print("\nDone!")
