import csv
import ipaddress
import os
import subprocess
import sys

from datetime import datetime


ip_ranges_csv = "ip_ranges.csv"
ports_csv = "ports.csv"


def read_source_ip(config_path):
    with open(config_path, "r") as file:
        return file.read().strip()


def expand_ip_range(ip_range):
    expanded_ips = []
    if "-" in ip_range:
        start_ip, end_ip = ip_range.split("-")
        start_ip = ipaddress.ip_address(start_ip)
        end_ip = ipaddress.ip_address(end_ip)
        while int(start_ip) <= int(end_ip):
            expanded_ips.append(str(start_ip))
            start_ip += 1
    else:
        try:
            network = ipaddress.ip_network(ip_range, strict=False)
            for ip in network.hosts():
                expanded_ips.append(str(ip))
        except ValueError:
            expanded_ips.append(ip_range)
    return expanded_ips


def expand_port_range(port_range):
    if "-" in port_range:
        start_port, end_port = map(int, port_range.split("-"))
        return list(range(start_port, end_port + 1))
    else:
        return [int(port_range)]


def load_csv(filename, expand_function):
    if not os.path.isfile(filename):
        print(f"Error: The file {filename} is missing.")
        sys.exit(1)

    items = []
    with open(filename, newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for item in row:
                items.extend(expand_function(item))
    return items


def run_hping3(ip, port):
    cmd = [
        "hping3",
        "-S",
        ip,
        "-p",
        str(port),
        "-c",
        "1",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout + result.stderr


def main():
    ip_ranges = load_csv(ip_ranges_csv, expand_ip_range)
    ports = load_csv(ports_csv, expand_port_range)

    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"scan_results_{current_time}.log"

    with open(log_filename, "w") as logfile:
        for ip in ip_ranges:
            for port in ports:
                print(f"Scanning {ip}:{port}...")
                log_output = run_hping3(ip, port)
                logfile.write(f"Scanning {ip}:{port}:\n{log_output}\n")

    print("Scan complete. Results saved to", log_filename)


if __name__ == "__main__":
    main()
