# FastAPI Dockerfile for Render with Python 3.10
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy all project files to container
COPY FastAPI_Backend /app/FastAPI_Backend

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r /app/FastAPI_Backend/requirements.txt

# Command to run app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
