<div align="center">

# 🎬 Open Caption by YO JI STUDIO

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![faster-whisper](https://img.shields.io/badge/faster--whisper-1.0.0-purple.svg)](https://github.com/SYSTRAN/faster-whisper)
[![Docker Support](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)](./Dockerfile)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](./LICENSE)

**高精度 AI 音视频自动字幕识别与硬字幕烧录工作站 (Apple Frosted Glass Edition)**

支持多文件批量处理、在线表格实时校对、全局查找替换、.SRT/.VTT/.ASS 多格式导出、NVENC 显卡 GPU 烧录加速、独立桌面 APP 窗口模式及 Docker 部署。

[🌟 核心特性](#-核心亮点与特性) • [🖥️ 桌面应用一键启动](#-windows-桌面成品应用一键启动) • [🐳 Docker 部署](#-docker-容器化部署) • [🎮 GPU 加速](#-nvidia-gpu-硬件加速推荐)

</div>

---

## 🌟 核心亮点与特性

1. **🖥️ 独立 Native Desktop App 窗口**：
   - 告别传统浏览器标签页，启动后自动拉起独立的极简 Native 桌面窗口，体验与 C++ / Electron 原生应用无异。

2. **⚡ 高速高精度离线 AI 引擎**：
   - 基于 `faster-whisper`，识别速度较原生 OpenAI Whisper 提升数倍。支持 `large-v3`, `large-v3-turbo`, `medium`, `small` 等全系列模型选配。

3. **🔍 全局查找与批量替换 (Batch Find & Replace)**：
   - 字幕表格支持全局一键搜索与批量替换，快速修正错别字与品牌名词。

4. **🎨 .ASS 高级特效字幕格式导出**：
   - 增加导出标准 Advanced SubStation Alpha (`.ass`) 格式，完美兼容 Pr、Final Cut Pro、DaVinci、剪映等专业剪辑软件。

5. **⚡ FFmpeg NVENC 显卡 GPU 烧录加速**：
   - 视频字幕硬烧录时自动识别 NVIDIA 显卡并开启 `h264_nvenc` 硬件编码器，烧录速度提升 5~10 倍！

6. **🎙️ Silero VAD 降噪静音过滤**：
   - 内置 VAD 静音检测机制，彻底避免无声区幻觉乱码或时间轴错位问题。

7. **🍏 苹果 macOS 极简毛玻璃美学 (Apple Frosted Glass)**：
   - 采用 San Francisco 系统字体，苹果 System Blue 配色与半透明毛玻璃暗黑材质。

---

## 🖥️ Windows 桌面成品应用一键启动

### 方式一：双击生成桌面快捷方式（最便捷）

1. 下载 / 解压项目代码。
2. 双击运行 **`一键创建桌面应用快捷方式.vbs`**。
3. 系统将在您的 Windows 桌面上生成专属的 **`Open Caption by YO JI STUDIO`** 图标快捷方式，以后直接双击桌面图标即可弹出独立应用窗口！

### 方式二：双击运行批处理

双击根目录下的 **`启动软件.bat`**，自动完成环境初始化并唤起桌面独立应用。

---

## 🐳 Docker 容器化部署

适合 NAS（群晖 / Unraid）、Linux 服务器或团队私有云一键部署：

```bash
# 克隆仓库
git clone https://github.com/your-username/Open-Caption.git
cd Open-Caption

# 启动容器 (自动挂载模型缓存)
docker compose up -d
```
启动后在浏览器中访问：`http://localhost:8000`

---

## 📦 打包为免环境 standalone `.exe` 程序

如果您想将本项目打包为无 Python 环境要求的单独立打包：

```bash
python build_exe.py
```
编译完成后，可在 `dist/Open_Caption_Studio/` 目录下得到 `Open_Caption_Studio.exe`。

---

## 🎮 NVIDIA GPU 硬件加速推荐

若您的设备配备 NVIDIA 显卡：

```bash
.venv\Scripts\python.exe -m pip install torch --index-url https://download.pytorch.org/whl/cu121
```

---

## 📄 开源许可证

本项目采用 [GNU General Public License v3.0 (GPL-3.0)](./LICENSE) 开源许可证。任何修改或基于本项目的二次开发作品**必须同样开源**。
