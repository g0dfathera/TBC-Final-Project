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

        # Convert the target IP to an IPv4Address object
        ip = ipaddress.IPv4Address(target_ip)

        # Check if the IP is within any of the private networks
        for network in private_networks:
            if ip in network:
                return True
        return False
    except ValueError:
        # If the IP address is invalid (not a valid IPv4 address)
        return False


def run_nmap_scan(target_ip, scan_depth):
    # Check if the target IP is part of an internal network
    if is_internal_ip(target_ip):
        return "Error: Scanning internal networks (private IPs) is not allowed."
    
    nm = nmap.PortScanner()

    try:
        # Modify the scan based on depth
        if scan_depth == "basic":
            nm.scan(target_ip)
        elif scan_depth == "service":
            nm.scan(target_ip, arguments="-sV")  # -sV flag for version detection
        elif scan_depth == "full":
            nm.scan(target_ip, arguments="-A")  # -A for OS detection, version, script scanning, and traceroute

        # Return the results as a dictionary or formatted string
        return nm.all_hosts(), nm[target_ip]
    except Exception as e:
        return f"Error: {e}"

# Example usage
target_ip = "example.com"  # Replace with your target IP or hostname
scan_depth = "full"  # Options: "basic", "service", "full"

scan_result = run_nmap_scan(target_ip, scan_depth)

# Format the result for better readability
if isinstance(scan_result, tuple):
    hosts, result = scan_result
    print(f"Hosts found: {hosts}")
    print(f"Scan result for {target_ip}:")
    print(result)
else:
    print(scan_result)
