# Use stable Python version
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all frontend code
COPY . .

# Upgrade pip and install requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Start Streamlit app
CMD ["streamlit", "run", "Generate_Recommendations.py", "--server.port=8501", "--server.enableCORS=false"]
