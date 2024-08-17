import os
from datetime import datetime, tzinfo, timezone
from pymongo import MongoClient
from dotenv import load_dotenv
from pprint import pprint
# Requires the PyMongo package.
# https://api.mongodb.com/python/current

load_dotenv()
MONGODB_URI = os.environ['MONGODB_URI']

uri = f"{MONGODB_URI}?retryWrites=true&w=majority&appName=mongo-to-bq"
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