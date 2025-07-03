FROM python:3.10-slim

# Install system build tools and missing dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    curl \
    libopenblas-dev \
    autoconf \
    automake \
    libtool \
    pkg-config \
    ninja-build \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY app/ app/
COPY models/ models/
COPY requirements.txt .

# Disable Metal for Intel CPU builds
ENV CMAKE_ARGS="-DLLAMA_METAL=OFF"

# Upgrade build tools
RUN pip install --upgrade pip setuptools wheel build

RUN pip install --upgrade pip setuptools wheel build \
    && pip install torch --index-url https://download.pytorch.org/whl/cpu \
    && pip install sentence-transformers==2.2.2 \
    && pip install -r requirements.txt
RUN pip install --no-binary :all: --no-cache-dir -r requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
