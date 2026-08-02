# -*- coding: utf-8 -*-
"""
Open Caption by YO JI STUDIO - Native Desktop Application Launcher
打开独立的 Native App 窗口 (Port 8000)，提供 100% 专有原生软件体验。
"""

import os
import sys
import time
import subprocess
import webbrowser
import urllib.request

APP_TITLE = "Open Caption by YO JI STUDIO"
PORT = 8000
URL = f"http://127.0.0.1:{PORT}"

def is_server_running(url: str) -> bool:
    try:
        response = urllib.request.urlopen(f"{url}/api/diagnose_hardware", timeout=1)
        return response.status == 200
    except Exception:
        return False

def launch_native_window(url: str):
    """
    唤起系统 Edge / Chrome 的 App 极简独立窗口模式 (--app=URL)
    """
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        os.path.expanduser(r"~\AppData\Local\Microsoft\Edge\Application\msedge.exe")
    ]
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
    ]

    browser_exe = None
    for p in edge_paths + chrome_paths:
        if os.path.exists(p):
            browser_exe = p
            break

    if browser_exe:
        try:
            subprocess.Popen([browser_exe, f"--app={url}", f"--name={APP_TITLE}"])
            return
        except Exception:
            pass

    webbrowser.open(url)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    server_py_path = os.path.join(script_dir, "server.py")

    python_exe = sys.executable

    # 启动 100% 专有 FastAPI 后台服务器
    cmd = [python_exe, server_py_path]
    server_process = subprocess.Popen(cmd, cwd=script_dir)

    # 等待服务就绪
    max_wait = 30
    start_time = time.time()
    while time.time() - start_time < max_wait:
        if is_server_running(URL):
            break
        time.sleep(0.5)

    # 唤起 Native 独立桌面窗口
    launch_native_window(URL)

    try:
        server_process.wait()
    except KeyboardInterrupt:
        server_process.terminate()

if __name__ == "__main__":
    main()
