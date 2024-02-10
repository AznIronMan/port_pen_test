# Port Pen Test Suite

Welcome to the Port Pen Test Suite, a comprehensive toolkit designed for network vulnerability scanning and penetration testing. Developed by ClarkTribeGames, this suite provides a set of tools to automate the process of finding open ports and attempting to brute force access with common credentials.

## Getting Started

These instructions will help you set up the Port Pen Test Suite on your local machine for development, testing, or security assessments. Please do so responsibly and ensure you have authorization before scanning any network.

### Prerequisites

Ensure that you have the following prerequisites installed on your system:

- Python 3.11.8 or later
- pip (Python package manager)

It's highly recommended to use a virtual environment to avoid conflicts with system-wide Python packages.

### Installation

To install the Port Pen Test Suite, follow these steps:

1. Clone the repository from GitHub:
   ```sh
   git clone https://github.com/AznIronMan/port_pen_test.git
   ```
2. Navigate to the root of the cloned directory.
3. If you are using a virtual environment, activate it. Otherwise, skip this step.
4. Install the required dependencies using pip:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

The Port Pen Test Suite consists of three Python scripts:

1. `brute_force.py` - Tries to connect to the provided IP addresses and ports using SSH or FTP with a list of known usernames and passwords.
2. `find_open_ports.py` - Scans a range of IP addresses and ports to determine if they are open.
3. `process_log.py` - Processes the output log from `find_open_ports.py` to create a CSV file suitable for `brute_force.py`.

### Running the Scripts

To scan for open ports:

```sh
python find_open_ports.py
```

After scanning, process the logs to find successful connections:

```sh
python process_log.py scan_results_sample.log
```

To perform brute-force testing on open ports:

```sh
python brute_force.py sample.csv
```

Replace `sample.csv` with the output CSV from `process_log.py`.

## Included Files

- `requirements.txt`: Contains the necessary Python packages required for the scripts.
- `usernames.txt` and `passwords.txt`: Starter packs of common usernames and passwords. For more extensive lists, consider repositories like [SecLists](https://github.com/danielmiessler/SecLists), [Kaonashi](https://github.com/kaonashi-passwords/Kaonashi), or [rockyou](https://github.com/zacheller/rockyou).
- `scan_results_sample.log`: Sample log file from running `find_open_ports.py`.
- `sample.csv`: Sample CSV file containing IP addresses and ports to test against.
- `ports.csv`: This CSV file specifies the ports to be scanned by `find_open_ports.py`. The current configuration supports ports 5800, 5900, 3389, 80, 21, and 22. While these are the primary ports for services such as VNC, RDP, HTTP, FTP, and SSH, you are welcome to modify the file to scan other ports.

## Notes

- The scripts are optimized for Python 3.11.8. Using the latest version of Python is recommended for the best compatibility.
- Network scanning and brute-forcing can be resource-intensive. Ensure that you have permission to test the network and that the target system can handle the load.
- The `brute_force.py` script will attempt to log in using SSH or FTP and will record successful logins in `success.csv`.

## Author Information

**Geoff Clark**

- [ClarkTribeGames](https://clarktribegames.com)
- Email: [geoff@gdv.llc](mailto:geoff@gdv.llc)
- [GitHub @aznironman](https://github.com/aznironman)
- [Instagram: @aznironman](https://instagram.com/aznironman)
- [Twitter: @aznironman](https://www.twitter.com/aznironman)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Third-Party Notices

All rights reserved by their respective owners. Users must comply with the licenses and terms of service of the software being installed.
