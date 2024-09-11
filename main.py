from fastapi import FastAPI, HTTPException
from google.cloud import pubsub_v1 as ps
from pydantic import RootModel
import os
import json

app = FastAPI()

# Configuration: Setting the environment variables in Cloud Run
port = int(os.getenv("PORT", 8088))
PROJECT_ID = os.getenv("PROJECT_ID")
TOPIC_ID = os.getenv("TOPIC_ID1")


# Initializing Pub/Sub Publisher
publisher = ps.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

class Message(RootModel[str]):
    # Define a generic message structure; adjust as needed
    pass

@app.post("/publish")
async def publish_message(message:Message):
    try:
        # Converting the message to JSON and encoding it as bytes
        message_json = json.dumps(message.__root__)
        message_bytes = message_json.encode("utf-8")

        # Publishing the message to Pub/Sub
        future = publisher.publish(topic_path, data=message_bytes)
        future.result() # Waiting for the message to be published

        return {"message":"Message published to Pub/Sub"}
    
    except Exception as e:
        print(f"Error publishing message: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    