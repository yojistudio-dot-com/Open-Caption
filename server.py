# -*- coding: utf-8 -*-
"""
Open Caption by YO JI STUDIO - 100% Zero-Dependency Custom Server (Standard Library)
无需任何第三方 Web 框架 (不用 FastAPI / Flask / Streamlit)，开箱即用 100% 稳定运行。
"""

import os
import re
import sys
import json
import time
import tempfile
import gc
import subprocess
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Tuple, Optional

# Windows CUDA DLL 修复
if sys.platform == "win32":
    torch_lib_dir = os.path.join(os.path.dirname(__file__), ".venv", "Lib", "site-packages", "torch", "lib")
    if os.path.exists(torch_lib_dir) and hasattr(os, "add_dll_directory"):
        try:
            os.add_dll_directory(torch_lib_dir)
        except Exception:
            pass
    if "PATH" in os.environ and os.path.exists(torch_lib_dir):
        os.environ["PATH"] = torch_lib_dir + os.path.pathsep + os.environ["PATH"]

import torch

try:
    from faster_whisper import WhisperModel
    HAS_FASTER_WHISPER = True
except ImportError:
    HAS_FASTER_WHISPER = False

try:
    import imageio_ffmpeg
    HAS_IMAGEIO_FFMPEG = True
except ImportError:
    HAS_IMAGEIO_FFMPEG = False

MODEL_CACHE = {}

def get_ffmpeg_executable() -> Optional[str]:
    try:
        res = subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0:
            return "ffmpeg"
    except Exception:
        pass

    if HAS_IMAGEIO_FFMPEG:
        try:
            exe_path = imageio_ffmpeg.get_ffmpeg_exe()
            if exe_path and os.path.exists(exe_path):
                return exe_path
        except Exception:
            pass

    return None

def get_recommended_model() -> Tuple[str, str, bool, str]:
    has_cuda = torch.cuda.is_available()
    if has_cuda:
        gpu_name = torch.cuda.get_device_name(0)
        try:
            vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        except Exception:
            vram_gb = 8.0

        if vram_gb >= 10:
            rec_model = "large-v3"
        elif vram_gb >= 6:
            rec_model = "large-v3-turbo"
        else:
            rec_model = "medium"
        return "cuda", f"GPU {gpu_name}", True, rec_model
    else:
        return "cpu", "CPU 计算模式", False, "medium"

class CustomAppRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        web_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")
        super().__init__(*args, directory=web_dir, **kwargs)

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)

        if parsed_url.path == "/api/diagnose_hardware":
            device, device_name, is_cuda, rec_model = get_recommended_model()
            ffmpeg_cmd = get_ffmpeg_executable()
            resp = {
                "device": device,
                "device_name": device_name,
                "is_cuda": is_cuda,
                "ffmpeg_ready": ffmpeg_cmd is not None,
                "recommended_model": rec_model
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode("utf-8"))
            return

        # 静态文件
        return super().do_GET()

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)

        if parsed_url.path == "/api/burn_video":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            payload = json.loads(post_data.decode("utf-8"))

            ffmpeg_cmd = get_ffmpeg_executable()
            if not ffmpeg_cmd:
                resp = {"success": False, "error": "未找到 FFmpeg 命令。"}
            else:
                resp = {"success": True, "msg": "准备就绪"}

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode("utf-8"))
            return

        if parsed_url.path == "/api/transcribe":
            # 基础转写示例响应
            resp = {
                "success": True,
                "results": {
                    "产品介绍视频.mp4": {
                        "segments": [
                            {"start": 2.0, "end": 5.0, "text": "大家好，欢迎来到 YO JI STUDIO 的 AI 字幕识别软件演示。"},
                            {"start": 5.0, "end": 9.0, "text": "今天我们来看看它的强大功能和简单易用的操作界面。"},
                            {"start": 9.0, "end": 12.3, "text": "支持多种格式导入，实时转写，精准高效。"},
                            {"start": 12.0, "end": 14.5, "text": "让我们开始体验吧！"}
                        ],
                        "duration": 14.5,
                        "language": "zh"
                    }
                }
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode("utf-8"))
            return

        self.send_error(404, "Endpoint Not Found")

def run(port=8000):
    server_address = ("127.0.0.1", port)
    httpd = HTTPServer(server_address, CustomAppRequestHandler)
    print(f"Open Caption Server running at http://127.0.0.1:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run(8000)
