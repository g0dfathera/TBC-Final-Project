#!/bin/bash
# Exit on error
set -e

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Check if nmap is installed, if not, install it
if ! command -v nmap &> /dev/null
then
    echo "nmap not found, installing nmap..."
    apt-get update && apt-get install -y nmap
else
    echo "nmap is already installed"
fi

# Check if yarn is installed, if not, install it
if ! command -v yarn &> /dev/null
then
    echo "Yarn not found, installing Yarn..."
    npm install -g yarn
else
    echo "Yarn is already installed"
fi

# Run any additional commands or build steps you need
echo "Running additional build steps..."

# If you need to run any other commands, you can add them below
# For example, if you want to run a custom build script or do something else

# Add your custom build steps here
