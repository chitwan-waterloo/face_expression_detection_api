# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install the smaller dependencies first
RUN pip install --no-cache-dir flask opencv-python-headless numpy keras flask-cors

# Install tensorflow separately with a longer timeout
RUN pip install --no-cache-dir --default-timeout=1000 tensorflow

# Copy the rest of the application code to /app
COPY . .

# Command to run the application
CMD ["python", "app.py"]