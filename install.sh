#!/bin/bash

command_exists() {
    command -v "$1" &> /dev/null
}

install_nmap_apt() {
    echo "Detected apt-based system (e.g., Ubuntu, Debian). Installing nmap..."
    sudo apt-get update
    sudo apt-get install -y nmap
}

install_nmap_yum() {
    echo "Detected yum-based system (e.g., CentOS, Fedora). Installing nmap..."
    sudo yum install -y nmap
}

install_nmap_pacman() {
    echo "Detected pacman-based system (e.g., Arch Linux). Installing nmap..."
    sudo pacman -Sy --noconfirm nmap
}

if command_exists apt; then
    install_nmap_apt
elif command_exists yum; then
    install_nmap_yum
elif command_exists pacman; then
    install_nmap_pacman
else
    echo "No compatible package manager found. Please install nmap manually."
    exit 1
fi

if command_exists nmap; then
    echo "nmap has been successfully installed."
else
    echo "Installation failed. Please check your system or package manager."
    exit 1
fi

pip install -r requirements.txt
