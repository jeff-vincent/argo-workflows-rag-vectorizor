import os
import pymongo


MONGO_PASSWORD = os.environ.get('MONGODB_PASSWORD')

def init_db():
    client = pymongo.MongoClient(f"mongodb+srv://jeffdvincent:{MONGO_PASSWORD}@cluster0.8xe9o.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client.admin_database
    rag_collection = db.rag

    # try:
    #     rag_collection.create_index("page_title", unique=True)
    # except Exception as e:
    #     print(f"Error creating indexes: {e}")

    
    return rag_collection

rag_collection = init_db()