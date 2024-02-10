import sys
import re
import csv

from datetime import datetime


def process_log_file(log_file_path):
    scan_pattern = re.compile(r"Scanning (\d+\.\d+\.\d+\.\d+):(\d+):")
    packet_loss_pattern = re.compile(r", (\d+)% packet loss")
    results = []
    with open(log_file_path, "r") as file:
        lines = file.readlines()
    current_ip = ""
    current_port = ""
    for line in lines:
        scan_match = scan_pattern.search(line)
        if scan_match:
            current_ip, current_port = scan_match.groups()
        packet_loss_match = packet_loss_pattern.search(line)
        if packet_loss_match:
            packet_loss = int(packet_loss_match.group(1))
            if packet_loss == 0:
                results.append((current_ip, current_port))

    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    with open(f"brute_ready_{current_time}.csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["ipaddress", "port"])
        for ip, port in results:
            writer.writerow([ip, port])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_log.py <log_file_path>")
        sys.exit(1)
    log_file_path = sys.argv[1]
    process_log_file(log_file_path)
