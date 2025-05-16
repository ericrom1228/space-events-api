# Use official Python slim base image
FROM python:3.12.10-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create a non-root user
RUN addgroup --system appuser && \
    adduser --system --ingroup appuser appuser

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
#    build-essential \
#    libffi-dev \
#    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies early to cache them
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Switch to non-root user
USER appuser

# Expose port (optional for documentation)
EXPOSE 3001

# Command to run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3001"]
