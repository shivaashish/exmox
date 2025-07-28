FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy the requirements file and install the dependencies
# Use a separate step to leverage Docker's layer caching
COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq-dev \
        build-essential && \
    pip install --no-cache-dir -r requirements.txt && \
    # Clean up APT cache to reduce image size
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "rover.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
