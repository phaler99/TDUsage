import psutil
import time

initial_data = {}
cached_connections = {}
last_connection_check = time.time()
connection_check_interval = 30  # секунды

def monitor_network_usage(interval=1, process_refresh_interval=30):
    global last_connection_check

    while True:
        current_time = time.time()

        if current_time - last_connection_check > connection_check_interval:
            last_connection_check = current_time
            new_cached_connections = {}

            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    pid = proc.pid
                    connections = proc.connections(kind='inet')

                    if connections:
                        new_cached_connections[pid] = connections
                        
                        if pid not in initial_data:
                            io_counters = proc.io_counters()
                            initial_data[pid] = (io_counters.write_bytes, io_counters.read_bytes)
                    else:
                        if pid in cached_connections:
                            del cached_connections[pid]

                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    if pid in cached_connections:
                        del cached_connections[pid]
                    if pid in initial_data:
                        del initial_data[pid]

            cached_connections.update(new_cached_connections)

        for pid, connections in cached_connections.items():
            try:
                proc = psutil.Process(pid)
                
                io_counters = proc.io_counters()
                current_sent = io_counters.write_bytes
                current_recv = io_counters.read_bytes
                
                prev_sent, prev_recv = initial_data.get(pid, (0, 0))
                
                data_sent = max(0, current_sent - prev_sent)
                data_recv = max(0, current_recv - prev_recv)
                
                initial_data[pid] = (current_sent, current_recv)
                
                if data_sent > 0 or data_recv > 0:
                    output = f"Process {proc.info['name']} (PID {pid}) sent {data_sent // 1024} KB, received {data_recv // 1024} KB"
                    print(output)
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                if pid in cached_connections:
                    del cached_connections[pid]
                if pid in initial_data:
                    del initial_data[pid]

        time.sleep(interval)

if __name__ == "__main__":
    monitor_network_usage()