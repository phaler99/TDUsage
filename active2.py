import time
import psutil
import win32gui
import win32process
import datetime
import json

session_template = {
    "timestamp": "",
    "duration": 0,
    "appname": ""
}

def save_time_append(filename, session_data):
    with open(filename, 'a') as f:
        for session in session_data:
            json.dump(session, f)
            f.write('\n')

def get_active_window_process():
    hwnd = win32gui.GetForegroundWindow()
    if hwnd == 0:
        return None, None
    _, pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
    return psutil.Process(pid), win32gui.GetForegroundWindow()

def track_active_process_append(interval, filename, flush_interval):
    last_pid = None
    duration = 0
    session_data = []
    last_flush_time = int(time.time())

    session_dict = session_template.copy()
    while True:
        current_time = time.time()

        active_process, hwnd = get_active_window_process()
        if not active_process:
            time.sleep(interval)
            continue

        current_pid = active_process.pid

        if active_process.name().lower() == "explorer.exe":
            window_title = win32gui.GetWindowText(hwnd).strip()
            if not window_title:
                time.sleep(interval)
                continue

        if current_pid != last_pid:
            if duration != 0:
                last_start_datetime = datetime.datetime.fromtimestamp(last_start_time)

                session_dict["timestamp"] = last_start_datetime.isoformat(timespec='seconds')
                session_dict["duration"] = duration
                session_dict["appname"] = last_process.name()
                session_data.append(session_dict.copy())

                print(f"Logged session: {last_process.name()}, Duration: {duration} seconds, Timestamp: {session_dict["timestamp"]}")

            last_pid = current_pid
            last_process = active_process
            last_start_time = current_time
            duration = 0

        duration = current_time - last_start_time

        if current_time - last_flush_time >= flush_interval:
            if session_data:
                save_time_append(filename, session_data)
                session_data.clear()
            last_flush_time = current_time

        time.sleep(interval)

track_active_process_append(1, "data.json", 5)
