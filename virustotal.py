import hashlib
import requests
import os
import base64

# VirusTotal API Key and URL
API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
BASE_URL = 'https://www.virustotal.com/api/v3'



def scan_url(url):
    headers = {'x-apikey': API_KEY}

    # First, encode the URL (URL encoding required by VirusTotal)
    url_id = hashlib.sha256(url.encode()).hexdigest()  # Simple encoding method (VirusTotal URL encode might be different)

    # Check if the URL scan result already exists in VirusTotal
    check_url = f'{BASE_URL}/urls/{url_id}'
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
