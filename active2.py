import time
import psutil
import win32gui
import win32process
import datetime
import json

def save_time_append(filename, start_time, duration, process_name):
    session_data = {
        "timestamp": start_time.isoformat(),
        "duration": duration,
        "appname": process_name
    }
    with open(filename, 'a') as f:
        json.dump(session_data, f)
        f.write('\n')

def get_active_window_process():
    if win32gui.GetForegroundWindow() == 0:
        return None, None
    _, pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
    return psutil.Process(pid), win32gui.GetForegroundWindow()

def track_active_process_append(interval, filename):
    last_pid = None
    duration = 0

    while True:
        current_datetime = datetime.datetime.now()

        active_process, hwnd = get_active_window_process()
        if not active_process:
            time.sleep(interval)
            continue

        current_pid = active_process.pid

        if active_process.name().lower() == "explorer.exe":
            window_title = win32gui.GetWindowText(hwnd).strip()
            if window_title == "":
                time.sleep(interval)
                continue

        if current_pid != last_pid:
            if duration != 0:
                save_time_append(filename, last_start_time, duration, last_process.name())
                print(f"Logged session: {last_process.name()}, Duration: {duration} seconds")

            last_pid = current_pid
            last_process = active_process
            last_start_time = current_datetime
            duration = 0

        duration += interval
        time.sleep(interval)

track_active_process_append(1, "data.json")
