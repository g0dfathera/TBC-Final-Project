#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Python dependencies
pip3 install -r requirements.txt

# Install nmap
if ! command -v nmap &> /dev/null
then
    echo "nmap not found, installing nmap..."
    apt-get update
    apt-get install -y nmap
else
    echo "nmap is already installed"
fi

# Any additional commands you need to run during the build
