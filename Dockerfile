# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies and other tools (if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean

# Install Node.js and Yarn globally
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g yarn

# Copy the current directory contents into the container at /app
COPY . /app

# Create a virtual environment and activate it
RUN python3 -m venv /venv

# Install Python dependencies inside the virtual environment
RUN /venv/bin/pip install --upgrade pip \
    && /venv/bin/pip install -r requirements.txt

# Set the environment variable to use the virtual environment
ENV PATH="/venv/bin:$PATH"

# Install Yarn dependencies (you can include this step if you are using Node.js)
RUN yarn install

# Expose the port the app runs on (if required)
EXPOSE 5000

# Command to run the app (adjust according to your project setup)
CMD ["python", "app.py"]
