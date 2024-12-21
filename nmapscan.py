import nmap

def run_nmap_scan(target_ip, scan_depth):
    try:
        # Initialize nmap PortScanner
        nm = nmap.PortScanner()

        # Running the nmap scan with version detection (-sV) and specified port range
        nm.scan(target_ip, scan_depth, '-sV')
        
        # Extracting scan result data
        scan_result = nm[target_ip]
        
        # Output the basic scan info
        print(f"Scan completed on: {scan_result['hostnames'][0]['name'] if 'hostnames' in scan_result else 'Unknown Hostname'}")
        print(f"Host IP: {scan_result['addresses']['ipv4']}")
        print(f"Host Status: {scan_result['status']['state']}")
        print(f"Scan Time: {nm.command_line()}")
        
        # Iterate over open TCP ports and display their information
        print("Open Ports and Services:")
        for port, port_data in scan_result['tcp'].items():
            if port_data['state'] == 'open':
                service_name = port_data['name']
                service_product = port_data.get('product', 'Unknown')
                print(f"  Port {port}: {service_name} ({service_product})")

        # Return the parsed scan result if needed for further processing
        return scan_result

    except nmap.nmap.PortScannerError as e:
        print(f"PortScannerError: {e}")
    except Exception as e:
        print(f"Error: {e}")
