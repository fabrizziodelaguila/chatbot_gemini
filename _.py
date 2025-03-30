from database import get_db

def test_db_connection():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT 1")
        print("Database connection successful")
    except Exception as e:
        print(f"Database connection failed: {str(e)}")

# Run this to test
test_db_connection()