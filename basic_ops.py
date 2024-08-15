import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv


# Load config from a .env file:
load_dotenv()
MONGODB_URI = os.environ['MONGODB_URI']


uri = f"{MONGODB_URI}?retryWrites=true&w=majority&appName=mongo-to-bq"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)