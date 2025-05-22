# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy all project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose both FastAPI (8000) and Streamlit (8501) ports
# EXPOSE 8000
EXPOSE 8501

# Set default command to run both apps in background
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port 8000 & streamlit run main.py --server.port=8501 --server.address=0.0.0.0"]
