<div align="center">

# 🎬 Open Caption by YO JI STUDIO

**High-Precision AI Audio/Video Subtitle Recognition & Video Burn-in Studio (Apple Frosted Glass UI)**
<br>
**高精度 AI 影视音视频自动字幕识别与硬字幕烧录工作站 (苹果极简毛玻璃界面)**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![faster-whisper](https://img.shields.io/badge/faster--whisper-1.0.0-purple.svg)](https://github.com/SYSTRAN/faster-whisper)
[![Docker Support](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)](./Dockerfile)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](./LICENSE)

[English Readme](#-english) • [中文说明](#-中文说明) • [Quickstart / 快速启动](#-quickstart--快速启动) • [Docker Deploy / Docker 部署](#-docker-deployment--docker-部署)

</div>

---

## 🌐 English

### Overview
**Open Caption by YO JI STUDIO** is a state-of-the-art, open-source AI desktop application and web workstation designed for high-precision audio/video speech-to-text transcription, subtitle proofreading, and video hardcode subtitle burn-in.

Powered by **faster-whisper**, **Silero VAD**, and **FFmpeg with NVIDIA NVENC GPU hardware acceleration**, it delivers 5x–10x faster processing than standard OpenAI Whisper while maintaining 100% data privacy with completely local offline execution.

### Key Features
- **⚡ Fast & Offline AI Engine**: Based on `faster-whisper` (`large-v3`, `large-v3-turbo`, `medium`, `small`, `base`, `tiny`).
- **🖥️ Standalone Native App Window**: Independent desktop application window without browser address bars.
- **🎙️ Silero VAD Silence Filtering**: Prevents hallucinations, misalignments, or phantom text in silent audio segments.
- **🔍 Batch Find & Replace**: Search and replace brand names or typos across all subtitle segments in one click.
- **🎨 Multi-Format Subtitle Export**: Export standard `.srt`, `.vtt`, `.ass` (Advanced SubStation Alpha), and plain text.
- **🔥 GPU Hardware Burn-In**: Accelerated video subtitle burn-in via FFmpeg `h264_nvenc` GPU encoding.
- **🌐 Multilingual UI (i18n)**: Real-time UI language switching between Chinese (🇨🇳), English (🇺🇸), and French (🇫🇷).
- **🍏 Apple Frosted Glass UI**: Modern dark space glassmorphism design system inspired by macOS.

---

## 🇨🇳 中文说明

### 项目概述
**Open Caption by YO JI STUDIO** 是一款专为影视创作者、自媒体、教育及会议记录打造的高精度本地离线 AI 字幕识别与硬字幕烧录工作站。

系统搭载 **faster-whisper** 大模型、**Silero VAD 语音降噪检测** 及 **FFmpeg NVENC 显卡 GPU 烧录加速**，识别速度比原生 OpenAI Whisper 提升数倍，数据 100% 本地处理，安全可靠。

### 核心亮点
- **⚡ 高速本地离线 AI 引擎**：基于 `faster-whisper`，全系列模型 (`large-v3`, `large-v3-turbo`, `medium` 等) 本地选配。
- **🖥️ 独立 Native 桌面窗口**：无浏览器地址栏的原生桌面应用观感。
- **🎙️ Silero VAD 降噪过滤**：彻底解决无声段落乱吐字或时间轴错位。
- **🔍 全局字幕查找与批量替换**：一键搜索与更正所有卡片中的专有名词与错别字。
- **🎨 多格式专业字幕导出**：支持导出 `.srt`、`.vtt`、`.ass` 特效字幕 (兼容 Pr / Final Cut / DaVinci / 剪映) 及无时间轴纯文本。
- **🔥 NVENC 显卡 GPU 烧录加速**：调用 NVIDIA 显卡硬件编码，视频合成速度提升 5~10 倍。
- **🌐 多语言 UI (中/英/法)**：支持中文 🇨🇳、English 🇺🇸、Français 🇫🇷 实时一键无缝切换。
- **🍏 苹果毛玻璃美学 UI**：深蓝紫流光与 24px 毛玻璃暗黑高阶设计。

---

## 🚀 Quickstart / 快速启动

### Option A: 1-Click Windows Desktop App (Windows 一键快捷方式)

1. Clone or download this repository / 下载解压本仓库。
2. Double-click **`一键创建桌面应用快捷方式.bat`**.
   - Automatically generates a desktop icon **`Open Caption by YO JI STUDIO`** on your Windows Desktop!
   - 双击运行即可在 Windows 桌面上自动生成带图标的快捷方式。
3. Double-click the desktop shortcut to launch the app! / 双击桌面图标即可弹出独立应用窗口。

---

## 🐳 Docker Deployment / Docker 部署

Ideal for self-hosters, NAS (Synology / Unraid), and Linux servers:

```bash
# Clone the repository
git clone https://github.com/your-username/Open-Caption.git
cd Open-Caption

# Build and run with Docker Compose (Volume mounts persistent model cache)
docker compose up -d
```
Access the web workstation at `http://localhost:8000`.

---

## 🎮 NVIDIA GPU Hardware Acceleration / GPU 显卡加速

To enable NVIDIA CUDA GPU acceleration and NVENC video burn-in speedup:

```bash
.venv\Scripts\python.exe -m pip install torch --index-url https://download.pytorch.org/whl/cu121
```

---

## 📁 Project Structure / 项目目录结构

```
Open-Caption/
├── web/                           # Custom HTML5 + CSS3 + JS Glassmorphism Frontend
│   ├── index.html                 # App DOM Layout
│   ├── style.css                  # Apple Glassmorphism & Mesh Gradient CSS
│   └── main.js                    # i18n & Client Logic
├── server.py                      # Pure Python Zero-Dependency Local API Server
├── desktop_app.py                 # Standalone Desktop Application Window Launcher
├── build_exe.py                   # PyInstaller EXE Packaging Automation
├── requirements.txt               # Python Dependencies
├── Dockerfile                     # Docker Build Recipe
├── docker-compose.yml             # Docker Compose Persistent Config
├── LICENSE                        # GNU General Public License v3.0 (GPL-3.0)
├── 启动软件.bat                   # Windows Launch Script
├── 一键创建桌面应用快捷方式.bat    # 1-Click Desktop Shortcut Generator
└── 准备开源到GitHub.bat           # 1-Click GitHub Repository Push Tool
```

---

## 🔍 SEO Keywords / 搜索引擎关键词
`whisper` `faster-whisper` `speech-to-text` `subtitle-generator` `video-captioning` `hardcode-subtitles` `ffmpeg` `nvenc` `ass-subtitles` `srt` `vtt` `bilingual-subtitles` `docker` `python` `open-source` `字幕识别` `语音识别` `视频字幕硬烧录` `双语字幕` `离线字幕生成` `ASS特效字幕`

---

## 📄 License / 开源许可证

Licensed under the **[GNU General Public License v3.0 (GPL-3.0)](./LICENSE)**. Any derivative work or modifications **must also be open-sourced** under GPL-3.0.
任何基于本项目的二次开发或修改作品**必须保持开源**。
