import socket
from common_ports import ports_and_services

def get_open_ports(target, port_range, verbose=False):
    open_ports = []

    # Resolve the target to an IP address
    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        if socket.inet_aton(target):
            return "Error: Invalid IP address"
        else:
            return "Error: Invalid hostname"

    # Scan the specified port range
    for port in range(port_range[0], port_range[1] + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        s.close()

    # Handle verbose output
    if verbose:
        service_lines = []
        for port in open_ports:
            service_name = ports_and_services.get(port, 'unknown')
            service_lines.append(f"{port:<9} {service_name}")
        
        url = target if target == ip else target
        output = f"Open ports for {url} ({ip})\nPORT     SERVICE\n"
        output += "\n".join(service_lines)
        return output

    return open_ports
