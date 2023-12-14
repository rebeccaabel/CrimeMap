from pymongo import MongoClient, IndexModel
from pymongo.errors import ConnectionFailure

# Load environment variables from .env
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Access environment variables
mongodb_uri = os.getenv("MONGODB_URI")

try:
    # MongoDB connection
    client = MongoClient(mongodb_uri)
    db = client["CrimeMap"]
    collection = db["crime_data"]

    # Drop the collection
    collection.drop()

    # Drop the index
    collection.drop_indexes()

    # Create a new index
    index_model = IndexModel([("date", 1)])  # Adjust the field and ordering as needed
    collection.create_indexes([index_model])

    print("Collection 'crime_data' and index dropped successfully.")

except ConnectionFailure as e:
    print(f"Failed to connect to MongoDB: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the MongoDB connection
    if "client" in locals():
        client.close()
