FROM node:18-slim as client-builder

# Set working directory for client build
WORKDIR /app/client

# Copy client package files
COPY client/package*.json ./

# Install client dependencies
RUN npm install

# Copy client source files
COPY client/ ./

# Build client
RUN npm run build

# Use Python image for the backend
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY agent.py get_token.py server.py ./
COPY utils/ ./utils/
COPY settings.json ./

# Copy client build from previous stage
COPY --from=client-builder /app/client/dist ./client/dist

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["python", "server.py"]
