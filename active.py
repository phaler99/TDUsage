import time
import psutil
import win32gui
import win32process
import datetime
import json

def load_data(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {
            "time_track": {},
            "data_track": {}
        }
    return data

def get_latest_session_id(data):
    current_datetime = datetime.datetime.now()
    year = current_datetime.strftime('%Y')
    month = current_datetime.strftime('%m')
    day = current_datetime.strftime('%d')
    hour = current_datetime.strftime('%H')

    latest_id = 0
    hour_data = data["time_track"].get(year, {}).get(month, {}).get(day, {}).get(hour, {})
    for session_id in hour_data.keys():
        latest_id = max(latest_id, int(session_id))

    return latest_id

def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=1)

def save_time(data, year, month, day, hour, last_session_id, last_start_time, duration, last_process):
    current_data = data["time_track"]
    for key in [year, month, day, hour]:
        if key not in current_data:
            current_data[key] = {}
        current_data = current_data[key]
    current_data[last_session_id] = {
        "timestamp": last_start_time.isoformat(),
        "duration": duration,
        "appname": last_process.name()
    }

def get_active_window_process():
    if win32gui.GetForegroundWindow() == 0:
        return None, None
    _, pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
    return psutil.Process(pid), win32gui.GetForegroundWindow()

def track_active_process(interval, filename):
    data = load_data(filename)
    duration = 0
    last_pid = None
    last_session_id = get_latest_session_id(data)
    while True:
        current_datetime = datetime.datetime.now()
        year = current_datetime.strftime('%Y')
        month = current_datetime.strftime('%m')
        day = current_datetime.strftime('%d')
        hour = current_datetime.strftime('%H')

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
            if (duration != 0):
                save_time(data, year, month, day, hour, last_session_id, last_start_time, duration, last_process)
                save_data(filename, data)

                print(f"Duration: {duration} seconds")
                duration = 0
            last_session_id+=1
            print(f"Session number {last_session_id}")
            print(f"Active process: {active_process.name()} (PID: {current_pid})")
            print(f"Year: {year}")
            print(f"Month: {month}")
            print(f"Day: {day}")
            print(f"Hour: {hour}")

            last_pid = current_pid
            last_process = active_process
            last_start_time = current_datetime
        duration += interval
        time.sleep(interval)
#commit