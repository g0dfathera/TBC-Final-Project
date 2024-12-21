# Use a Python image as a base image
FROM python:3.9-slim

# Install system dependencies required for both Python and Node.js
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    curl \
    gnupg2 \
    lsb-release \
    apt-transport-https \
    ca-certificates \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (You can adjust the version as necessary)
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs

# Install Yarn (for Node.js package management)
RUN npm install -g yarn

# Set the working directory inside the container
WORKDIR /app

# Copy all necessary files (including render-build.sh) into the container
COPY . /app

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Install Node.js dependencies (yarn will be used)
RUN yarn install

# Run render-build.sh after dependencies are installed (make sure it exists)
RUN sh render-build.sh

# Expose the port that your app will run on
EXPOSE 5000

# Define the command to run your app (example for Flask)
CMD ["gunicorn", "app:app"]
