import os
import json
import asyncio
import uvicorn
from pymongo import MongoClient
from bson import json_util
from dotenv import load_dotenv
from urllib.parse import quote_plus
from fastapi import FastAPI
from google.cloud import pubsub_v1
from datetime import datetime

load_dotenv()
MONGODB_URI = os.getenv('MONGODB_URI')
MONGO_CLUSTER = os.getenv('MONGO_CLUSTER')
MONGO_DATA_BASE = os.getenv('MONGO_DATA_BASE')
PROJECT_ID = os.getenv("PROJECT_ID")
TOPIC_ID1 = os.getenv('TOPIC_ID1')
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/nombauser/Desktop/trying-pubsub-2024-663b6e06baf8.json'

cluster = quote_plus(f'{MONGO_CLUSTER}')
database = quote_plus(f'{MONGO_DATA_BASE}')
collection = "wallet_transactions"

uri = f'{MONGODB_URI}{database}?retryWrites=true&w=majority'
client = MongoClient(uri)
myCollection = client[f'{database}'][f'{collection}']

app = FastAPI()


# Pub/Sub publisher
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID1)
def publish_to_pubsub(data):
    """
    Publishes a message to a Pub/Sub topic.
    """
    try:
        data = json.dumps(data).encode("utf-8")
        future = publisher.publish(topic_path, data)
        print(f"Published message: {data}")
        print("Message sent successfully")
        return future.result()
    
    except Exception as e:
        print(f"error: {e}")


async def listen_to_changes():
    """
    Listens to the MongoDB change stream and publishes changes to Pub/Sub.
    """
    print("*_"*30)
    try:
        # Open the MongoDB change stream
        with myCollection.watch(full_document='updateLookup') as stream:
            print("Listening for changes...")
            for change in stream:
                # The 'change' document contains details of the operation
                change = json.dumps(change, default=json_util.default)
                print(f"Received change: {change}")
                publish_to_pubsub(change)
    except Exception as e:
        print(f"Error: {e}")


@app.get("/")
async def index():
    return {"message": "Cloud Run with FastAPI is running!"}



if __name__ == "__main__":
    # Run the change stream listener in the background
    asyncio.run(listen_to_changes())
    # Run the FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=8000)
