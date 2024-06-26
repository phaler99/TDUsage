import time
import psutil
import win32gui
import win32process
import datetime

current_datetime = datetime.datetime.now()

def get_active_window_process():
    if win32gui.GetForegroundWindow() == 0:
        return None, None
    _, pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
    return psutil.Process(pid), win32gui.GetForegroundWindow()

def track_active_process(interval=1):
    duration = 0
    last_pid = None
    while True:
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
                print(f"Duration: {duration} seconds")
                duration = 0

            print(f"Active process: {active_process.name()} (PID: {current_pid})")
            print(f"Year: {current_datetime.strftime('%Y')}")
            print(f"Month: {current_datetime.strftime('%m')}")
            print(f"Day: {current_datetime.strftime('%d')}")
            print(f"Hour: {current_datetime.strftime('%H')}")

            last_pid = current_pid
        duration += 1
        time.sleep(interval)

track_active_process()