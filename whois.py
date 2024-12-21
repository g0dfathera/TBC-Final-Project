import subprocess
from nmap import is_internal_ip

def run_whois_search(target_ip):
    # WHOIS search logic
    if is_internal_ip(target_ip):
        return "Error: WHOIS lookup for internal IPs is not allowed."

    try:
        # Execute WHOIS command
        command = ["whois", target_ip]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"
