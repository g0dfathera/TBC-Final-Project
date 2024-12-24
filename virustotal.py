import hashlib
import requests
import os
import base64
import time

API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
BASE_URL = 'https://www.virustotal.com/api/v3'


def scan_url(url):
    headers = {'x-apikey': API_KEY}
    encoded_url = base64.urlsafe_b64encode(url.encode()).decode().strip("=")  # Correct base64 encoding
    check_url = f'{BASE_URL}/urls/{encoded_url}'
    response = requests.get(check_url, headers=headers)

    if response.status_code == 200:
        result = response.json()
        return result
    elif response.status_code == 404:
        encoded_url = base64.urlsafe_b64encode(url.encode()).decode().strip("=")  # VirusTotal requires base64 encoding
        submit_url = f'{BASE_URL}/urls'
        response = requests.post(submit_url, headers=headers, data={'url': encoded_url})

        if response.status_code == 200:
            result = response.json()
            return result
        else:
            return None
    return None
