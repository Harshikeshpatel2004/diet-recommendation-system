FROM python:3.10.13-slim

# Step 1: Install system tools required to build numpy/pandas
RUN apt-get update && apt-get install -y build-essential

# Step 2: Create working directory
RUN mkdir -p /app/backend

# Step 3: Copy files
COPY FastAPI_Backend/requirements.txt /app/backend/requirements.txt
COPY Data /app/Data
COPY FastAPI_Backend /app/backend

# Step 4: Set working directory
WORKDIR /app/backend

# Step 5: Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Step 6: Expose backend port
EXPOSE 8080

# Step 7: Start the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
