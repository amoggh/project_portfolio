
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def test_mongodb_connection():
    try:
        # Connect to MongoDB server on localhost (default port 27017)
        client = MongoClient("mongodb://localhost:27017")
        db = client["portify_db"]  # Database name
        users_collection = db["users"]
        
        # Test the connection by listing databases
        databases = client.list_database_names()
        print("Connection successful!")
        print("Databases available:", databases)
        
    except ConnectionFailure as e:
        print(f"Connection failed: {e}")
    finally:
        # Close the connection
        client.close()

if __name__ == "__main__":
    test_mongodb_connection()
