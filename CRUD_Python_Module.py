"""Project One CRUD module adapted for the Project Two dashboard."""
from pymongo import MongoClient


class AnimalShelter:
    """Access the aac animals collection using authenticated MongoDB queries."""

    def __init__(self, username, password, host="localhost", port=27017,
                 database="aac", collection="animals", auth_source="aac"):
        # Keyword credentials avoid URI escaping problems with special characters.
        self.client = MongoClient(host=host, port=port, username=username,
                                  password=password, authSource=auth_source,
                                  serverSelectionTimeoutMS=5000)
        self.database = self.client[database]
        self.collection = self.database[collection]

    def close(self):
        """Release the database connection when finished."""
        self.client.close()

    # Implement the C in CRUD.
    def create(self, data):
        """Insert a document into the animals collection."""
        if data is not None:
            try:
                self.collection.insert_one(data)
                return True
            except Exception as e:
                print("Error inserting document:", e)
                return False
        else:
            return False

    def read(self, query, projection=None):
        """Return matching records; propagate database errors to the controller."""
        if not isinstance(query, dict):
            raise TypeError("query must be a dictionary; use {} for all records")
        return list(self.collection.find(query, projection))

    # Implement the U in CRUD.
    def update(self, query, update_data):
        """Update documents in the animals collection."""
        if query is not None and update_data is not None:
            try:
                result = self.collection.update_many(
                    query,
                    {"$set": update_data}
                )
                return result.modified_count
            except Exception as e:
                print("Error updating documents:", e)
                return 0
        else:
            return 0

    # Implement the D in CRUD.
    def delete(self, query):
        """Delete documents from the animals collection."""
        if query is not None:
            try:
                result = self.collection.delete_many(query)
                return result.deleted_count
            except Exception as e:
                print("Error deleting documents:", e)
                return 0
        else:
            return 0