#!/usr/bin/env python


import os
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1

PROJECT_ID = os.environ['PROJECT_ID']
SUBSCRIPTION1 = os.environ['SUBSCRIPTION1']
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/nombauser/Desktop/trying-pubsub-2024-663b6e06baf8.json'


timeout = None # seconds to wait for new messages (set to None for indefinite listening)

# Subscriber client
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION1)

def callback(message):
    print(f"Received message: {message.data}")
    message.ack()  # Acknowledge the message

# Listening for messages
streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}...\n")

# Keep the subscriber alive
with subscriber:
    try:
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()
