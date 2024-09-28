import time
import psutil
import win32gui
import win32process
import datetime
import json

def save_time_append(filename, session_data):
    with open(filename, 'a') as f:
        for session in session_data:
            json.dump(session, f)
            f.write('\n')

def get_active_window_process():
    if win32gui.GetForegroundWindow() == 0:
        return None, None
    _, pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
    return psutil.Process(pid), win32gui.GetForegroundWindow()

def track_active_process_append(interval, filename, flush_interval):
    last_pid = None
    duration = 0
    session_data = []
    last_flush_time = time.time()

    while True:
        current_time = time.time()

        active_process, hwnd = get_active_window_process()
        if not active_process:
            time.sleep(interval)
            continue

        current_pid = active_process.pid

        if active_process.name().lower() == "explorer.exe" and not win32gui.GetWindowText(hwnd).strip():
            time.sleep(interval)
            continue

        if current_pid != last_pid:
            if duration != 0:
                last_start_datetime = datetime.datetime.fromtimestamp(last_start_time)

                session_data.append({
                    "timestamp": last_start_datetime.isoformat(),
                    "duration": duration,
                    "appname": last_process.name()
                })
                print(f"Logged session: {last_process.name()}, Duration: {duration} seconds, Timestamp: {last_start_datetime}")

            last_pid = current_pid
            last_process = active_process
            last_start_time = current_time
            duration = 0

        duration = int(current_time - last_start_time)

        if current_time - last_flush_time >= flush_interval:
            if session_data:
                save_time_append(filename, session_data)
                session_data.clear()
            last_flush_time = current_time

        time.sleep(interval)

track_active_process_append(1, "data.json", 5)
