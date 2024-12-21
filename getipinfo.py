import requests

def get_ip_info(ip):
    # Validate the IP address format
    octets = ip.split(".")
    if len(octets) != 4:
        return {"error": "Invalid IPv4 address format"}

    for octet in octets:
        if not octet.isdigit():
            return {"error": "Invalid IPv4 address format"}
        num = int(octet)
        if num < 0 or num > 255:
            return {"error": "Invalid IPv4 address format"}

    try:
        # Make the API request to get IP information
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()

        if data.get("status") == "fail":
            return {"error": "Failed to get information for this IP"}

        # Construct the data to return
        return {
            "ip": data.get("query"),
            "country": data.get("country"),
            "region": data.get("regionName"),
            "city": data.get("city"),
            "org": data.get("org"),
            "isp": data.get("isp"),
            "loc": f"{data.get('lat', 'N/A')}, {data.get('lon', 'N/A')}",
            "postal": data.get("zip"),
            "timezone": data.get("timezone"),
            "as": data.get("as"),
            "error": None
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}
