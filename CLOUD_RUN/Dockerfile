# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt first to leverage Docker's caching mechanism
COPY requirements.txt .

# Install any necessary dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app will run on
EXPOSE 8088

# # Environment variables for MongoDB and Google Cloud Pub/Sub
# ENV MONGODB_URI=<your_mongodb_uri>
# ENV MONGO_CLUSTER=<your_mongo_cluster>
# ENV MONGO_DATA_BASE=<your_database_name>
# ENV PROJECT_ID=<your_project_id>
# ENV TOPIC_ID1=<your_topic_id1>

# # Set the Google Application Credentials environment variable
# ENV GOOGLE_APPLICATION_CREDENTIALS=/app/trying-pubsub-2024-663b6e06baf8.json

# Run the FastAPI app using Uvicorn
CMD ["uvicorn", "watch_changeStream:app", "--host", "0.0.0.0", "--port", "8088"]