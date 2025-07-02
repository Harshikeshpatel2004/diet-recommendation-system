FROM python:3.10-slim

# Install build tools & update pip
RUN apt-get update && apt-get install -y build-essential && pip install --upgrade pip

# Create and set working directory
WORKDIR /app

# Copy source and install dependencies
COPY Streamlit_Frontend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY Streamlit_Frontend ./

# Expose default port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "Generate_Recommendation.py", "--server.port=8501", "--server.enableCORS=false"]
