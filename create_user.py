import os
import pymongo
import secrets

# MONGO_PASSWORD = os.environ.get('MONGODB_PASSWORD')
MONGODB_PASSWORD = 'USmmDHouYrxATnSJ'

def init_db():
    client = pymongo.MongoClient(f"mongodb+srv://jeffdvincent:{MONGODB_PASSWORD}@cluster0.8xe9o.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client.admin_database
    rag__user_collection = db.rag_users
    
    return rag__user_collection

rag_user_collection = init_db()

def create_user():
    api_key = secrets.token_hex(16)
    user = {
        'api_key': api_key,
        'allowed_origins': ['http://localhost:3000', 'http://localhost', 'http://localhost:8000'],
    }
    rag_user_collection.insert_one(user)
    return user

create_user()
