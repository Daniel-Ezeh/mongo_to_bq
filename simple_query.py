import os
from datetime import datetime, timezone
from pymongo import MongoClient
from dotenv import load_dotenv
from pprint import pprint
from urllib.parse import quote_plus

# Requires the PyMongo package.
# https://api.mongodb.com/python/current

load_dotenv()
MONGODB_URI = os.environ['MONGODB_URI']
MONGO_DATA_BASE = os.environ['MONGO_DATA_BASE']

database = quote_plus(f'{MONGO_DATA_BASE}')

uri = f'{MONGODB_URI}{database}?retryWrites=true&w=majority'
client = MongoClient(uri)
myCollection = client['sample_mflix']['embedded_movies']

# Create a new client and connect to the server
filter={
    'released': {
        '$gte': datetime(1914, 1, 1, 0, 0, 0, tzinfo=timezone.utc), 
        '$lte': datetime(1920, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
    }
}

projection = {
    "plot":1,
    "genres":1,
    "production":1,
    "writers":1,
    "countries":1,
}


result = myCollection.find_one(
  filter=filter,
  projection=projection
)

pprint(result)