import nmap
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

    nm = nmap.PortScanner()

    try:
        if scan_depth == "basic":
            # Run a fast scan with fewer ports (-F flag)
            result = nm.scan(target_ip, arguments="-F")
        elif scan_depth == "service":
            # Run a scan with service version detection (-T4 -sV flags)
            result = nm.scan(target_ip, arguments="-T4 -sV")

        return result
    except Exception as e:
        return f"Error: {str(e)}"
