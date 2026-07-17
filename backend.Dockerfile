# Use a lightweight, official Python runtime image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the operational workspace directory
WORKDIR /workspace

# Install system utilities if needed (e.g., git or curl for healthchecks)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency requirements matrix and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the core system codebase array into the working path
COPY ./app /workspace/app
COPY ./outputs /workspace/outputs

# Expose the internal network gateway port
EXPOSE 8000

# Fire up the production ASGI production instance bound to all interfaces
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]