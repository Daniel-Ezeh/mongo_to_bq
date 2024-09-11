# using the official lightweight Python image
FROM  python:3.10-slim

# Setting the environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Setting the working directory inside the container
WORKDIR /app

# Installing dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Coping the application code
COPY . .

# Exposing the port that FastAPI will run on
EXPOSE 8088

# The command to run the FastAPI app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8088"]
