# Use an official Node.js image as the base image
FROM node:16

# Install necessary system dependencies (e.g., nmap, Python, etc.)
RUN apt-get update && apt-get install -y \
    nmap \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and install node dependencies
COPY package.json /app/

# Install dependencies using npm if no yarn.lock file exists
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
