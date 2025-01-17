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
&& rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip setuptools wheel
# cargo \
# git \

# Copy the current directory contents into the container
COPY . /app

# RUN pip install --upgrade --no-cache-dir --only-binary=:all: -r requirements.txt
RUN pip install --upgrade --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir numpy==1.21.6 spacy==3.4.4 thinc==8.1.9

RUN python -m spacy validate

# Expose port 8000 for Flask
EXPOSE 8000

# Run the application
CMD ["python", "app.py"]