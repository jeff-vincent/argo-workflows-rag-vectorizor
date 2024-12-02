import os
import pymongo


# MONGO_PASSWORD = os.environ.get('MONGODB_PASSWORD')
MONGODB_PASSWORD = ''

def init_db():
    client = pymongo.MongoClient(f"mongodb+srv://jeffdvincent:{MONGODB_PASSWORD}@cluster0.8xe9o.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client.admin_database
    users_collection = db.rag_users
    
    return users_collection

users_collection = init_db()