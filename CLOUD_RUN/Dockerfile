# Use an official Python runtime as a base image

FROM python:3.10-alpine

# Allow statements and log messages to immediately appear in the Cloud Run logs
ENV PYTHONUNBUFFERED True


# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt first to leverage Docker's caching mechanism

COPY requirements.txt ./


# Install any necessary dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container

COPY . ./



# # Expose the port the app will run on
EXPOSE 8088



# Run the FastAPI app using Uvicorn
CMD ["uvicorn", "watch_changeStream:app", "--host", "0.0.0.0", "--port", "8088"]