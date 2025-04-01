import os
import psutil
import requests
import time

from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import win32gui
import win32process

# Configure logging

# Server URL (consider making this configurable in production)
SERVER_URL = "http://192.168.1.6:8000/api/data"

# Get computer ID (Windows HWID)
def get_computer_id():
    """Returns the Windows device name (computer name)."""
    return os.environ['COMPUTERNAME']

# Collect metrics (UTC+8 timezone)
def get_windowed_pids():
    """Get PIDs of processes with visible windows."""
    windowed_pids = set()

    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != "":
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            windowed_pids.add(pid)
        return True

    win32gui.EnumWindows(callback, None)
    return windowed_pids

def collect_metrics():
    """Collect metrics only for windowed apps."""
    windowed_pids = get_windowed_pids()
    timestamp = datetime.now(timezone.utc).astimezone(ZoneInfo("Asia/Shanghai")).isoformat()

    cpu_percent = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    apps = {}

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'create_time']):
        try:
            # Skip non-windowed processes
            if proc.info['pid'] not in windowed_pids:
                continue

            app_name = proc.info['name']
            duration = int(time.time() - proc.info['create_time'])

            apps[app_name] = {
                "duration": duration,
                "cpu": proc.info['cpu_percent'],
                "ram": proc.info['memory_percent']
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return {
        "computer_id": get_computer_id(),
        "username": os.getlogin(),
        "timestamp": timestamp,
        "cpu": cpu_percent,
        "ram": {
            "total": ram.total,
            "used": ram.used,
            "percent": ram.percent
        },
        "apps": apps
    }

# Send data to server
def send_metrics():
    data = collect_metrics()
    headers = {"User-Agent": "CloudMonitorAgent/1.0", "Content-Type": "application/json"}
    try:
        response = requests.post(SERVER_URL, json=data, headers=headers)
        response.raise_for_status()  # Raises an exception for HTTP errors (e.g., 404, 500)
    except requests.exceptions.RequestException as e:
        print(f"Failed to send metrics: {e}")  # Temporary output; could be replaced with retry logic

if __name__ == "__main__":
    while True:
        send_metrics()
        time.sleep(300)  # 5 minutes