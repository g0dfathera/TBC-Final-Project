import requests
import json
import os
import ipaddress
import dotenv

API_KEY = os.getenv("WHOIS_API_KEY")

def is_internal_ip(target_ip):
    try:
        private_networks = [
            ipaddress.IPv4Network("10.0.0.0/8"),
            ipaddress.IPv4Network("172.16.0.0/12"),
            ipaddress.IPv4Network("192.168.0.0/16"),
            ipaddress.IPv4Network("169.254.0.0/16")
        ]

        ip = ipaddress.IPv4Address(target_ip)

        for network in private_networks:
            if ip in network:
                return True
        return False
    except ValueError:
        return False

def run_whois_search(target_ip):
    if is_internal_ip(target_ip):
        return "Error: WHOIS lookup for internal IPs is not allowed."

    try:
        url = f'https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey={API_KEY}&domainName={target_ip}&outputFormat=JSON'

        response = requests.get(url)

        # Check if the response is successful
        if response.status_code == 200:
            whois_data = response.json()

            def clean_whois_data(whois_data):
                record = whois_data.get('WhoisRecord', {})

                # Extract the necessary fields from the raw WHOIS response
                cleaned_whois = {
                    "Domain Name": record.get('domainName', 'Not available'),
                    "Creation Date": record.get('registryData', {}).get('createdDate', 'Not available'),
                    "Expiration Date": record.get('registryData', {}).get('expiresDate', 'Not available'),
                    "Registrar": record.get('registrarName', 'Not available'),
                    "Registrar IANA ID": record.get('registrarIANAID', 'Not available'),
                    "Estimated Domain Age": record.get('estimatedDomainAge', 'Not available'),
                    "Name Servers": ", ".join(record.get('registryData', {}).get('nameServers', {}).get('hostNames', [])),
                    "Audit Created Date": record.get('audit', {}).get('createdDate', 'Not available'),
                    "Audit Updated Date": record.get('audit', {}).get('updatedDate', 'Not available')
                }

                registrant = record.get('registryData', {}).get('registrant', {})
                cleaned_whois["Registrant"] = {
                    "Name": registrant.get('name', 'Not available'),
                    "Email": registrant.get('email', 'Not available')
                }

                tech_contact = record.get('registryData', {}).get('technicalContact', {})
                cleaned_whois["Technical Contact"] = {
                    "Name": tech_contact.get('name', 'Not available'),
                    "Email": tech_contact.get('email', 'Not available')
                }

                admin_contact = record.get('registryData', {}).get('administrativeContact', {})
                cleaned_whois["Administrative Contact"] = {
                    "Name": admin_contact.get('name', 'Not available'),
                    "Email": admin_contact.get('email', 'Not available')
                }

                return cleaned_whois

            cleaned_whois = clean_whois_data(whois_data)

            formatted_output = "\n--- WHOIS Lookup Results ---\n"
            for key, value in cleaned_whois.items():
                if isinstance(value, dict):
                    formatted_output += f"\n{key}:\n"
                    for sub_key, sub_value in value.items():
                        formatted_output += f"  {sub_key}: {sub_value}\n"
                else:
                    formatted_output += f"{key}: {value}\n"

            return formatted_output

        else:
            return f"Error: Unable to fetch WHOIS data for {target_ip}. Status Code: {response.status_code}"

    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

    whois_info = run_whois_search(target_ip)
    print(whois_info)
