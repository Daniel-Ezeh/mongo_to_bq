import os
import random_user_gen as ru
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGODB_URI = os.environ['MONGODB_URI']

uri = f"{MONGODB_URI}?retryWrites=true&w=majority&appName=mongo-to-bq"
client = MongoClient(uri)
myCollection = client['customers']['wallet_transactions']


customer = ru.get_random_user()

insert = myCollection.insert_one(
    customer
)