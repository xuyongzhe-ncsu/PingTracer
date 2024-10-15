# PingTracer
**PingTracer** is a Python tool that allows you to ping multiple IPv4/IPv6 addresses concurrently (to be implemented) and trace the route to responsive addresses using ICMP packets. 

## Requirements

- Python 3.9 or higher
- Scapy library

## Installation

1. **Go to root dir**:
    ```bash
    cd root
    ```

2. **Install package**:
    You can use `pip3` to install the package. All necessary dependencies will automatically installed.
    ```bash
    pip3 install -e .
    ```

3. **Run sample code**:
    Note that `sudo` is necessary to enable a ping
    ```bash
    sudo python3 main.py
    ```