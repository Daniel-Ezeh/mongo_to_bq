# Use an official Python runtime as a base image
FROM python:3.10-slim

# Allow statements and log messages to immediately appear in the Cloud Run logs
ENV PYTHONUNBUFFERED=True

# Setting the environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Setting the working directory inside the container
WORKDIR /app

# Copy the requirements.txt first to leverage Docker's caching mechanism
COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . ./

# Exposing the port that FastAPI will run on
EXPOSE 8088

# Run the application
CMD ["python3", "watch_changeStream.py"]
# CMD exec uvicorn watch_changeStream:app --port 8088 --host 0.0.0.0