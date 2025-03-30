import os
import winreg

import psutil
import requests
import uuid
import time
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import win32gui
import win32process

# Server URL
SERVER_URL = "http://localhost:8000/api/data"


# Get computer ID (Windows HWID)
def get_computer_id():
    try:
        hwid = uuid.getnode()  # Get hardware ID
        return str(uuid.uuid5(uuid.NAMESPACE_OID, str(hwid)))
    except:
        return str(uuid.uuid4())


# Add to Windows startup
def add_to_startup():
    try:
        key = winreg.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(key, key_path, 0, winreg.KEY_WRITE) as reg_key:
            exe_path = os.path.abspath("agent.exe")
            winreg.SetValueEx(reg_key, "CloudMonitorAgent", 0, winreg.REG_SZ, exe_path)
    except Exception as e:
        print(f"Startup error: {e}")


# Collect metrics (UTC+8 timezone)
def get_windowed_pids():
    """Get PIDs of processes with visible windows"""
    windowed_pids = set()

    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != "":
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            windowed_pids.add(pid)
        return True

    win32gui.EnumWindows(callback, None)
    return windowed_pids


def collect_metrics():
    """Collect metrics only for windowed apps"""
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
        "computer_id": str(uuid.uuid5(uuid.NAMESPACE_OID, str(uuid.getnode()))),
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
        print(f"Status: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    add_to_startup()
    while True:
        send_metrics()
        time.sleep(300)  # 5 minutes