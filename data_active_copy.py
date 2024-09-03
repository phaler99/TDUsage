import psutil
import time

initial_data = {}
cached_connections = {}

def monitor_network_usage(interval=1, process_refresh_interval=60):
    last_refresh_time = 0
    processes = []
    data_sent = 0
    data_recv = 0


    while True:
        current_time = time.time()
        
        # Обновляем список процессов каждые process_refresh_interval секунд
        if current_time - last_refresh_time > process_refresh_interval:
            processes = list(psutil.process_iter(['pid', 'name']))
            last_refresh_time = current_time
        
        for proc in processes:
            try:
                connections = proc.net_connections(kind='inet')
                if not connections:
                    continue

                if proc.pid not in initial_data:
                    initial_data[proc.pid] = proc.io_counters().write_bytes, proc.io_counters().read_bytes

                io_counters = proc.io_counters()
                current_sent = io_counters.write_bytes
                current_recv = io_counters.read_bytes

                prev_sent, prev_recv = initial_data[proc.pid]

                if prev_sent != current_sent or prev_recv != current_recv:
                    data_sent = max(0, current_sent - prev_sent)
                    data_recv = max(0, current_recv - prev_recv)

                initial_data[proc.pid] = current_sent, current_recv

                if data_sent > 0 or data_recv > 0:
                    output = f"Process {proc.info['name']} (PID {proc.pid}) sent {data_sent // 1024} KB, received {data_recv // 1024} KB"
                    print(output)

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        time.sleep(interval)

if __name__ == "__main__":
    monitor_network_usage()
