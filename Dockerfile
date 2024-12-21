# Use an official Node.js image as the base image
FROM node:16

# Install necessary system dependencies (e.g., nmap, Python, etc.)
RUN apt-get update && apt-get install -y \
    nmap \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy package.json to the container
COPY package.json /app/

# Check if yarn.lock exists and copy it if it does
COPY yarn.lock /app/ || echo "No yarn.lock file found"

# Install dependencies using yarn or npm
RUN if [ -f yarn.lock ]; then yarn install; else npm install; fi

# Install Python dependencies (if any)
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

# Copy the rest of your application code to the container
COPY . /app/

# Copy the render-build.sh script to the container and make it executable
COPY render-build.sh /app/
RUN chmod +x /app/render-build.sh

# Run the render-install.sh script
RUN sh /app/render-build.sh

# Expose the port your app runs on (replace with the correct port if necessary)
EXPOSE 3000

# Define the command to run your application (e.g., using npm start)
CMD ["npm", "start"]
