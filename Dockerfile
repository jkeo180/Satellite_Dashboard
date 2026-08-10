FROM python:3.11-slim

# Install system utilities
RUN apt-get update && apt-get install -y \
    build-essential \
    libgeos-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Explicitly upgrade pip and install dependencies globally
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Verify installation paths during build step
RUN which streamlit || echo "Streamlit executable path check failed"

COPY . .

# Force target port and bind address mapping
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
