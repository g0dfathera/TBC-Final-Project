# Website about Penetration Testing and it's tools

Welcome to the **Penetration Testing Tools Website**! This web application offers a range of built-in tools designed for penetration testing and security analysis. Users can perform actions such as network scanning, WHOIS lookups, VirusTotal scanning, and more, all while maintaining a history of their results.

# Accessing Website

You can access website on this URL - https://tbc-final-project-1.onrender.com/
(on this version of application nmap scanning feature isn't working due to Permission error. You can build fully functional version on your machine too! scroll down to learn how to build it on your own)

## Features

- **Nmap Lookup**: Perform network scans to discover devices, services, and open ports on a target system.
- **WHOIS Lookup**: Get domain registration details, including owner information and registration dates.
- **VirusTotal URL Scanning**: Scan URLs to check for potential security threats using the VirusTotal API.
- **IP Lookup**: Gather information about a specific IP address, including geolocation and network details.
- **Result History**: Every scan or lookup performed is saved to an SQL database, and users can view their previous scan results through a dedicated history page.

## Technologies Used

- **Backend**: Python (Flask, SQLAlchemy)
- **Frontend**: HTML/Bootstrap
- **Database**: SQLite (SQL database for storing users and their results)
- **Containerization**: Docker (to enable cross-platform deployment)
- **Networking Tools**: Nmap, WHOIS, VirusTotal API, IP lookup tools
- **Security**: Penetration testing tools and secure result storage

### Requirements

- Docker (for cross-platform compatibility on Windows)
- Python 3.x
- Pip

### Running the Application

1. **Clone the repository:**

   ```bash
   git clone https://github.com/g0dfathera/TBC-Final-Project
   cd TBC-Final-Project
   ```
2. **Build the Docker image:**

   ```bash
   docker build -t penetration-tools-website .
   ```
3. **Run the Docker container:**

   ```bash
   docker run -p 5000:5000 penetration-tools-website
   ```
4. **Visit the web application in your browser at http://localhost:5000**

### License

This project is open-source and available under the MIT License.
