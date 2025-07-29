import pyautogui
import pygetwindow as gw
import pyttsx3
import requests
import os
import time
import datetime
import platform
import socket
import webbrowser
import subprocess

def say(args):
    print(*args)

def speak(args):
    engine = pyttsx3.init()
    engine.say(' '.join(str(a) for a in args))
    engine.runAndWait()

def read_file(args):
    filename = args[0]
    with open(filename, 'r') as f:
        return [f.read()]

def write_file(args):
    filename, content = args[0], args[1]
    with open(filename, 'w') as f:
        f.write(content)
    return [f"Wrote to {filename}"]

def append_file(args):
    filename, content = args[0], args[1]
    with open(filename, 'a') as f:
        f.write(content)
    return [f"Appended to {filename}"]

def http_get(args):
    url = args[0]
    response = requests.get(url)
    return [response.text]

def get_tabs(args):
    return [w.title for w in gw.getWindowsWithTitle('') if w.title]

def screenshot(args):
    path = args[0] if args else 'screenshot.png'
    pyautogui.screenshot(path)
    return [f"Saved screenshot to {path}"]

def sleep(args):
    t = float(args[0])
    time.sleep(t)
    return [f"Slept for {t} seconds"]

def now(args):
    return [datetime.datetime.now().isoformat()]

def sys_info(args):
    return [platform.platform()]

def hostname(args):
    return [socket.gethostname()]

def open_url(args):
    url = args[0]
    webbrowser.open(url)
    return [f"Opened {url}"]

def run_cmd(args):
    cmd = ' '.join(args)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return [result.stdout.strip()]

builtins = {
    "say": say,
    "speak": speak,
    "read_file": read_file,
    "write_file": write_file,
    "append_file": append_file,
    "http_get": http_get,
    "get_tabs": get_tabs,
    "screenshot": screenshot,
    "sleep": sleep,
    "now": now,
    "sys_info": sys_info,
    "hostname": hostname,
    "open_url": open_url,
    "run_cmd": run_cmd,
}
