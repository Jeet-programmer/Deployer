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

# Expose FastAPI on 8000 and Streamlit on 8051 (main)
EXPOSE 8000

# Run both services; Streamlit on port 8051 (main)
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port 8001 & streamlit run main.py --server.port=8000 --server.address=0.0.0.0"]
