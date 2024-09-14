# using the official lightweight Python image
FROM  python:3.10-slim

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

# Installing dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Coping the application code
COPY . .

# Exposing the port that FastAPI will run on
EXPOSE 8088

# The command to run the FastAPI app using uvicorn
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8088", "app:app"]
