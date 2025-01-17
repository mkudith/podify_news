# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app


# Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y \
build-essential \
libffi-dev \
libssl-dev \
python3-dev \
cargo \
git \
&& rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip setuptools wheel

# Copy the current directory contents into the container
COPY . /app

# RUN pip install --upgrade --no-cache-dir --only-binary=:all: -r requirements.txt
RUN pip install --upgrade --no-cache-dir -r requirements.txt

# Expose port 8000 for Flask
EXPOSE 8000

# Run the application
CMD ["python", "app.py"]