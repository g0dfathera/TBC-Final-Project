#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Python dependencies (assuming you have a requirements.txt)
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Install nmap (only if not already installed)
if ! command -v nmap &> /dev/null
then
    echo "nmap not found, installing nmap..."
    apt-get update
    apt-get install -y nmap
else
    echo "nmap is already installed"
fi

# Any additional setup steps can be added here (if necessary)
# For example, setting up environment variables, additional packages, etc.

# Output a message indicating the script has finished
echo "Render installation script has completed successfully!"
