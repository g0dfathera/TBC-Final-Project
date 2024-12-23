import subprocess
import ipaddress

def is_internal_ip(target_ip):

    try:
        # Define the private IP address ranges
        private_networks = [
            ipaddress.IPv4Network("10.0.0.0/8"),           # 10.x.x.x
            ipaddress.IPv4Network("172.16.0.0/12"),        # 172.16.x.x - 172.31.x.x
            ipaddress.IPv4Network("192.168.0.0/16"),       # 192.168.x.x
            ipaddress.IPv4Network("169.254.0.0/16")        # Link-local addresses (169.254.x.x)
        ]

        ip = ipaddress.IPv4Address(target_ip)

        for network in private_networks:
            if ip in network:
                return True
        return False
    except ValueError:
        return False


def run_nmap_scan(target_ip, scan_depth):

    if is_internal_ip(target_ip):
        return "Error: Scanning internal networks (private IPs) is not allowed."

    try:
        command = ["nmap"]

        if scan_depth == "basic":
            command.append(target_ip)
        elif scan_depth == "service":
            command.extend(["-sV", target_ip])  # -sV flag for version detection

        result = subprocess.run(command, capture_output=True, text=True, check=True)

        return result.stdout
    except subprocess.CalledProcessError as e:
        if "TCP/IP fingerprinting" in e.stderr:
            return "Error: OS scan requires root privileges."
        return f"Error: {e.stderr}"
