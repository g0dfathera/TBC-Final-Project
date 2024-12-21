#!/bin/bash
# Install nmap
apt install -y nmap

# Upgrade pip to the latest version
pip install --upgrade pip

# Install Python dependencies from requirements.txt
pip install -r requirements.txt
