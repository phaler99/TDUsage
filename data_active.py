import psutil
from datetime import datetime
from scapy.all import sniff, IP
from collections import defaultdict

# Initialize nested defaultdict
data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {'sent': 0, 'received': 0})))))

# Get initial network interface addresses
interface_addresses = {interface: addrs[0].address for interface, addrs in psutil.net_if_addrs().items() if addrs}

# Function to get process info
def get_process_info():
    process_info = {}
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            process_info[proc.info['pid']] = proc.info['name']
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return process_info

# Function to handle packets
def packet_callback(packet):
    if IP in packet:
        process_info = get_process_info()
        connections = psutil.net_connections(kind='inet')
        packet_pid = None

        for conn in connections:
            if conn.pid and isinstance(conn.laddr, tuple) and isinstance(conn.raddr, tuple):
                laddr_ip, laddr_port = conn.laddr
                raddr_ip, raddr_port = conn.raddr if conn.raddr else (None, None)

                if (laddr_ip == packet[IP].src and laddr_port == packet[IP].sport) or \
                   (raddr_ip == packet[IP].dst and raddr_port == packet[IP].dport):
                    packet_pid = conn.pid
                    break

        if packet_pid and packet_pid in process_info:
            process_name = process_info[packet_pid]
            now = datetime.now()
            year, month, day, hour = now.year, now.month, now.day, now.hour

            # Initialize nested dictionaries if not present
            if process_name not in data['data_track'][year][month][day][hour]:
                data['data_track'][year][month][day][hour][process_name] = {'sent': 0, 'received': 0}

            # Ensure nested dictionaries exist and update data
            if packet[IP].src in interface_addresses.values():
                data['data_track'][year][month][day][hour][process_name]['sent'] += len(packet)
            else:
                data['data_track'][year][month][day][hour][process_name]['received'] += len(packet)

# Function to monitor network usage
def monitor_network_usage():
    sniff(prn=packet_callback, store=0)

if __name__ == "__main__":
    monitor_network_usage()
    print(data)