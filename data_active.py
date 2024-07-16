import psutil
import time

def get_network_usage_per_app():
    usage = {}
    for proc in psutil.process_iter(['pid', 'name', 'io_counters']):
        try:
            io_counters = proc.info['io_counters']
            if io_counters:
                usage[proc.info['name']] = {
                    'bytes_sent': io_counters.bytes_sent,
                    'bytes_recv': io_counters.bytes_recv
                }
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return usage

def track_usage(interval):
    previous_usage = get_network_usage_per_app()
    while True:
        time.sleep(interval)
        current_usage = get_network_usage_per_app()
        
        for app in current_usage:
            if app in previous_usage:
                sent = current_usage[app]['bytes_sent'] - previous_usage[app]['bytes_sent']
                recv = current_usage[app]['bytes_recv'] - previous_usage[app]['bytes_recv']
                print(f"{app}: Sent {sent} bytes, Received {recv} bytes")
            else:
                print(f"{app}: Sent {current_usage[app]['bytes_sent']} bytes, Received {current_usage[app]['bytes_recv']} bytes")
        
        previous_usage = current_usage

track_usage(5)