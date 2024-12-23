FROM python:3.11-slim

RUN if command -v apt-get > /dev/null 2>&1; then \
        apt-get update && apt-get install -y nmap; \
    elif command -v yum > /dev/null 2>&1; then \
        yum install -y nmap; \
    else \
        echo "Neither apt-get nor yum found. Please install nmap manually."; \
        exit 1; \
    fi

RUN pip install -r requirements.txt
