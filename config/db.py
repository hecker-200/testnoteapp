from pymongo import MongoClient

MONGO_URI = 'mongodb+srv://b23es1003_db_user:achu2005@cluster0.qu8fgxf.mongodb.net/'

# Connect to MongoDB
conn = MongoClient(MONGO_URI)

# Access database and collection
db = conn.notes   # Database 'notes'
collection = db.notes  # Collection 'notes'
