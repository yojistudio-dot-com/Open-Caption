# -*- coding: utf-8 -*-
"""
===============================================================================
Open Caption by YO JI STUDIO - 智能字幕识别与硬字幕烧录工作站 (Vibrant Glass Edition)
===============================================================================
"""

import os
import re
import sys
import tempfile
import zipfile
import io
import time
import gc
import base64
import subprocess
from typing import List, Dict, Any, Tuple, Optional

# ===============================================================================
# 0. Windows CUDA DLL 环境变量修复
# ===============================================================================
if sys.platform == "win32":
    torch_lib_dir = os.path.join(os.path.dirname(__file__), ".venv", "Lib", "site-packages", "torch", "lib")
    if os.path.exists(torch_lib_dir) and hasattr(os, "add_dll_directory"):
        try:
            os.add_dll_directory(torch_lib_dir)
        except Exception:
            pass
    if "PATH" in os.environ and os.path.exists(torch_lib_dir):
        os.environ["PATH"] = torch_lib_dir + os.path.pathsep + os.environ["PATH"]

import streamlit as st
import pandas as pd
import torch

# 尝试导入 faster_whisper
try:
    from faster_whisper import WhisperModel
    HAS_FASTER_WHISPER = True
except ImportError:
    HAS_FASTER_WHISPER = False

# 尝试导入 imageio_ffmpeg 自动获取内置 static ffmpeg
try:
    import imageio_ffmpeg
    HAS_IMAGEIO_FFMPEG = True
except ImportError:
    HAS_IMAGEIO_FFMPEG = False


# ===============================================================================
# 1. 页面配置与参考图极致毛玻璃 UI 布局 (Deep Blue/Purple Mesh + Glowing Pill Sliders)
# ===============================================================================
LOGO_PATH = os.path.join(os.path.dirname(__file__), "logo.png")

st.set_page_config(
    page_title="Open Caption by YO JI STUDIO",
    page_icon=LOGO_PATH if os.path.exists(LOGO_PATH) else "🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_logo_base64() -> str:
    if os.path.exists(LOGO_PATH):
        try:
            with open(LOGO_PATH, "rb") as f:
                return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
        except Exception:
            pass
    return ""

LOGO_BASE64 = get_logo_base64()

# 参考图同款炫彩毛玻璃 CSS
CUSTOM_CSS = """
<style>
    /* 1. 彻底隐藏 Streamlit 默认页眉页脚 */
    #MainMenu, header, footer, .stDeployButton, [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"], #stDecoration {
        visibility: hidden !important;
        display: none !important;
    }
    
    /* 2. 全局深蓝紫流光梦幻背景 (与参考图 100% 一致) */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Segoe UI", Roboto, sans-serif !important;
        -webkit-font-smoothing: antialiased;
    }

    .stApp {
        background: radial-gradient(circle at 15% 15%, #251654 0%, #0a0f2b 50%, #030614 100%);
        background-attachment: fixed;
        color: #f2f4fc;
    }
    
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 93% !important;
    }

    /* 3. 极简滚动条 */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.18);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.3);
    }
    
    /* 4. 侧边栏 (Refined Translucent Sidebar) */
    [data-testid="stSidebar"] {
        background: rgba(12, 17, 43, 0.55) !important;
        backdrop-filter: blur(28px) saturate(200%) !important;
        -webkit-backdrop-filter: blur(28px) saturate(200%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0.8rem;
    }

    /* 5. 顶栏 Header (与参考图卡片风格一致) */
    .hero-glass-card {
        background: rgba(20, 28, 66, 0.45);
        backdrop-filter: blur(24px) saturate(180%);
        -webkit-backdrop-filter: blur(24px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 24px;
        padding: 24px 30px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.35);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.5px;
        margin: 0;
        line-height: 1.2;
    }
    .hero-subtitle {
        color: #989eba;
        font-size: 1rem;
        margin-top: 5px;
        font-weight: 400;
    }
    .hero-logo-img {
        width: 72px;
        height: 72px;
        border-radius: 18px;
        object-fit: cover;
        border: 1px solid rgba(255, 255, 255, 0.18);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }

    /* 6. 参考图同款状态控件与发光进度滑块 (Glowing Widget Pills) */
    .widget-tile {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 18px;
        padding: 14px 18px;
        margin-bottom: 12px;
    }
    .widget-label {
        font-size: 0.8rem;
        color: #989eba;
        font-weight: 500;
        margin-bottom: 6px;
    }
    .widget-value {
        font-size: 1.05rem;
        color: #ffffff;
        font-weight: 700;
    }
    
    /* 发光渐变进度条 (如参考图 Warm Orange & Cyan 胶囊) */
    .glow-bar-warm {
        height: 12px;
        border-radius: 10px;
        background: linear-gradient(90deg, #ff9500 0%, #ff3b30 100%);
        box-shadow: 0 0 12px rgba(255, 149, 0, 0.5);
        margin-top: 8px;
    }
    .glow-bar-cyan {
        height: 12px;
        border-radius: 10px;
        background: linear-gradient(90deg, #30b0c7 0%, #007aff 100%);
        box-shadow: 0 0 12px rgba(48, 176, 199, 0.5);
        margin-top: 8px;
    }
    .glow-bar-purple {
        height: 12px;
        border-radius: 10px;
        background: linear-gradient(90deg, #af52de 0%, #5856d6 100%);
        box-shadow: 0 0 12px rgba(175, 82, 222, 0.5);
        margin-top: 8px;
    }

    /* 7. 参考图同款按钮 (Vibrant Accent Buttons) */
    .stButton > button {
        background: linear-gradient(90deg, #007aff 0%, #30b0c7 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 12px 28px !important;
        font-weight: 700 !important;
        font-size: 0.98rem !important;
        letter-spacing: -0.2px !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 6px 20px rgba(0, 122, 255, 0.35) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 28px rgba(0, 122, 255, 0.55) !important;
    }
    .stDownloadButton > button {
        background: rgba(255, 255, 255, 0.08) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 16px !important;
        font-weight: 600 !important;
        backdrop-filter: blur(12px) !important;
        transition: all 0.2s ease !important;
    }
    .stDownloadButton > button:hover {
        background: rgba(255, 255, 255, 0.16) !important;
        border-color: rgba(255, 255, 255, 0.25) !important;
    }

    /* 8. 拖拽文件框 Dropzone */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px dashed rgba(255, 255, 255, 0.18);
        border-radius: 20px;
        padding: 20px;
        backdrop-filter: blur(16px);
        transition: all 0.25s ease;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #30b0c7;
        background: rgba(255, 255, 255, 0.06);
    }

    /* 9. 实时字幕预览卡片 */
    .stream-preview-card {
        background: rgba(20, 28, 66, 0.45);
        backdrop-filter: blur(24px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 20px;
        margin-top: 16px;
    }
    .subtitle-row {
        background: rgba(255, 255, 255, 0.05);
        border-left: 4px solid #30b0c7;
        padding: 12px 16px;
        margin-bottom: 10px;
        border-radius: 6px 12px 12px 6px;
    }
    .subtitle-time {
        color: #989eba;
        font-size: 0.82rem;
        font-family: SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        margin-bottom: 4px;
    }
    .subtitle-text {
        color: #ffffff;
        font-size: 1.02rem;
        font-weight: 500;
    }

    /* 10. 参考图同款顶栏 Tab 导航 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        color: #989eba;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 0 20px;
        font-size: 0.92rem;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, rgba(0, 122, 255, 0.3) 0%, rgba(48, 176, 199, 0.3) 100%) !important;
        color: #ffffff !important;
        border-color: rgba(48, 176, 199, 0.5) !important;
        box-shadow: 0 4px 16px rgba(0, 122, 255, 0.25);
    }

    .footer-text {
        text-align: center;
        color: #6a7196;
        font-size: 0.85rem;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ===============================================================================
# 2. 硬件检测与模型加载工具
# ===============================================================================
@st.cache_resource(show_spinner=False)
def check_hardware_environment() -> Tuple[str, str, str, bool]:
    has_cuda = torch.cuda.is_available()
    if has_cuda:
        gpu_name = torch.cuda.get_device_name(0)
        return "cuda", "float16", f"NVIDIA GPU: {gpu_name}", True
    else:
        return "cpu", "int8", "CPU 计算模式", False

@st.cache_resource(show_spinner=False)
def load_whisper_model(model_name: str, device: str, compute_type: str):
    if not HAS_FASTER_WHISPER:
        raise RuntimeError("未安装 faster-whisper 库，请运行 pip install faster-whisper 安装。")
    
    model = WhisperModel(
        model_size_or_path=model_name,
        device=device,
        compute_type=compute_type,
        download_root=os.path.join(os.path.expanduser("~"), ".cache", "whisper")
    )
    return model

def clear_vram():
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


# ===============================================================================
# 3. 字幕格式化工具 (SRT, VTT, ASS, 纯文本, 智能分行)
# ===============================================================================
def format_timestamp(seconds: float, format_type: str = "srt") -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    
    if millis >= 1000:
        secs += 1
        millis = 0
    if secs >= 60:
        minutes += 1
        secs = 0
    if minutes >= 60:
        hours += 1
        minutes = 0

    if format_type == "ass":
        centisecs = millis // 10
        return f"{hours}:{minutes:02d}:{secs:02d}.{centisecs:02d}"

    sep = "," if format_type == "srt" else "."
    return f"{hours:02d}:{minutes:02d}:{secs:02d}{sep}{millis:03d}"

def split_text_by_width(text: str, max_width: int = 35) -> List[str]:
    text = text.strip()
    if not text or len(text) <= max_width:
        return [text] if text else []
    
    lines = []
    current_line = ""
    words = re.split(r'(\s+)', text)
    
    for word in words:
        if len(current_line) + len(word) <= max_width:
            current_line += word
        else:
            if current_line.strip():
                lines.append(current_line.strip())
            current_line = word
            
    if current_line.strip():
        lines.append(current_line.strip())
        
    return lines if lines else [text]

def generate_srt_content(segments: List[Dict[str, Any]]) -> str:
    srt_lines = []
    index = 1
    for seg in segments:
        start_str = format_timestamp(seg['start'], 'srt')
        end_str = format_timestamp(seg['end'], 'srt')
        text = seg['text'].strip()
        if not text:
            continue
        srt_lines.append(f"{index}\n{start_str} --> {end_str}\n{text}\n")
        index += 1
    return "\n".join(srt_lines)

def generate_vtt_content(segments: List[Dict[str, Any]]) -> str:
    vtt_lines = ["WEBVTT\n"]
    for seg in segments:
        start_str = format_timestamp(seg['start'], 'vtt')
        end_str = format_timestamp(seg['end'], 'vtt')
        text = seg['text'].strip()
        if not text:
            continue
        vtt_lines.append(f"{start_str} --> {end_str}\n{text}\n")
    return "\n".join(vtt_lines)

def generate_ass_content(segments: List[Dict[str, Any]], title: str = "Open Caption") -> str:
    ass_header = f"""[Script Info]
Title: {title}
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,2,1,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    dialogues = []
    for seg in segments:
        start_str = format_timestamp(seg['start'], 'ass')
        end_str = format_timestamp(seg['end'], 'ass')
        text = seg['text'].strip().replace("\n", "\\N")
        if not text:
            continue
        dialogues.append(f"Dialogue: 0,{start_str},{end_str},Default,,0,0,0,,{text}")
        
    return ass_header + "\n".join(dialogues)

def generate_plain_text(segments: List[Dict[str, Any]]) -> str:
    return "\n".join([seg['text'].strip() for seg in segments if seg['text'].strip()])


# ===============================================================================
# 4. FFmpeg 视频字幕硬烧录函数 (支持 NVENC GPU 加速)
# ===============================================================================
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

def check_ffmpeg_available() -> bool:
    return get_ffmpeg_executable() is not None

def burn_subtitles_to_video(
    video_path: str,
    srt_path: str,
    output_video_path: str,
    font_size: int = 20,
    font_color: str = "&H00FFFFFF",
    outline_color: str = "&H00000000",
    use_nvenc: bool = False
) -> Tuple[bool, str]:
    ffmpeg_cmd = get_ffmpeg_executable()
    if not ffmpeg_cmd:
        return False, "未找到 FFmpeg 组件，请检查环境配置。"

    try:
        norm_srt = os.path.abspath(srt_path).replace("\\", "/")
        if ":" in norm_srt:
            drive, rest = norm_srt.split(":", 1)
            escaped_srt = f"{drive}\\:{rest}"
        else:
            escaped_srt = norm_srt

        style = f"FontSize={font_size},PrimaryColour={font_color},OutlineColour={outline_color},BorderStyle=1,Outline=2"
        vf_param = f"subtitles='{escaped_srt}':force_style='{style}'"

        video_codec_args = ["-c:v", "h264_nvenc", "-preset", "p4"] if use_nvenc else []

        cmd = [
            ffmpeg_cmd,
            "-y",
            "-i", video_path,
            "-vf", vf_param,
            *video_codec_args,
            "-c:a", "copy",
            output_video_path
        ]

        process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='ignore')

        if process.returncode == 0 and os.path.exists(output_video_path):
            return True, "烧录成功"
        else:
            if use_nvenc:
                return burn_subtitles_to_video(video_path, srt_path, output_video_path, font_size, font_color, outline_color, use_nvenc=False)
            return False, f"FFmpeg 烧录异常: {process.stderr[-400:]}"
            
    except Exception as e:
        return False, f"处理硬烧录时发生错误: {str(e)}"


# ===============================================================================
# 5. 主程序逻辑与 Streamlit UI 布局
# ===============================================================================
def main():
    sys_device, sys_compute, sys_device_name, is_nvenc_ready = check_hardware_environment()
    ffmpeg_ready = check_ffmpeg_available()

    logo_html = f'<img src="{LOGO_BASE64}" class="hero-logo-img">' if LOGO_BASE64 else '🎬'
    
    st.markdown(f"""
        <div class='hero-glass-card'>
            <div>
                <h1 class='hero-title'>Open Caption</h1>
                <div class='hero-subtitle'>by YO JI STUDIO • 高精度智能字幕识别与硬字幕烧录工作站</div>
            </div>
            <div>
                {logo_html}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 参考图同款状态 Widget 块 (3列排布)
    col_w1, col_w2, col_w3 = st.columns(3)
    with col_w1:
        st.markdown(f"""
            <div class='widget-tile'>
                <div class='widget-label'>硬件加速状态 (Device Mode)</div>
                <div class='widget-value'>{sys_device_name}</div>
                <div class='glow-bar-cyan'></div>
            </div>
        """, unsafe_allow_html=True)
    with col_w2:
        st.markdown(f"""
            <div class='widget-tile'>
                <div class='widget-label'>FFmpeg 烧录引擎 (Media Engine)</div>
                <div class='widget-value'>{"已就绪 (支持视频合成)" if ffmpeg_ready else "未就绪"}</div>
                <div class='glow-bar-warm'></div>
            </div>
        """, unsafe_allow_html=True)
    with col_w3:
        st.markdown(f"""
            <div class='widget-tile'>
                <div class='widget-label'>NVENC GPU 编码加速</div>
                <div class='widget-value'>{"支持 (5~10x 极速)" if is_nvenc_ready else "CPU 编码模式"}</div>
                <div class='glow-bar-purple'></div>
            </div>
        """, unsafe_allow_html=True)

    # ===========================================================================
    # 侧边栏配置
    # ===========================================================================
    with st.sidebar:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=100)
            
        st.markdown("<h4 style='color: #ffffff; font-weight: 600; font-size: 1rem;'>系统参数设置</h4>", unsafe_allow_html=True)
        
        # 1. 模型选择
        model_name = st.selectbox(
            "Whisper 模型规格",
            options=["large-v3", "large-v3-turbo", "medium", "small", "base", "tiny"],
            index=0,
            help="推荐 large-v3 获取最高准确率；或使用 large-v3-turbo 快速识别。"
        )

        # 2. 设备与计算精度选择
        device = st.selectbox(
            "运行计算设备",
            options=["cuda", "cpu"] if sys_device == "cuda" else ["cpu"],
            index=0
        )
        
        compute_type = st.selectbox(
            "计算精度模式",
            options=["float16", "int8", "float32"] if device == "cuda" else ["int8", "float32"],
            index=0
        )

        st.divider()
        st.markdown("<h4 style='color: #ffffff; font-weight: 600; font-size: 1rem;'>识别与断句微调</h4>", unsafe_allow_html=True)

        # 3. 任务类型与语言设置
        task = st.selectbox(
            "处理任务类型",
            options=["transcribe", "translate"],
            format_func=lambda x: "语音转写" if x == "transcribe" else "翻译为英文",
            index=0
        )

        language_options = {
            "自动识别 (Auto)": None,
            "中文": "zh",
            "英文": "en",
            "日语": "ja",
            "韩语": "ko",
            "法语": "fr",
            "德语": "de",
            "西班牙语": "es"
        }
        selected_lang_label = st.selectbox("主语言环境", list(language_options.keys()), index=0)
        language_code = language_options[selected_lang_label]

        # 4. VAD 过滤配置
        use_vad = st.checkbox("开启 Silero VAD 静音过滤", value=True)
        min_silence_ms = st.slider("最小断句间隔 (ms)", min_value=200, max_value=1500, value=500, step=50)

        # 5. Prompt 提示词
        initial_prompt = st.text_area(
            "文本规范提示词 (Prompt)",
            value="以下是普通话和英文的无缝对话，请添加标点符号，简体中文。",
            height=70,
            help="输入常用词汇或专业术语提示模型输出。"
        )

        # 6. 单行最大字数
        max_line_width = st.number_input("单行字幕最大字数", min_value=10, max_value=100, value=35, step=5)

    # ===========================================================================
    # 主区域：文件上传与识别控制
    # ===========================================================================
    uploaded_files = st.file_uploader(
        "选择或拖拽媒体文件至此处 (支持多文件批量上传)",
        type=["mp4", "mkv", "mov", "avi", "webm", "mp3", "wav", "m4a", "flac", "aac"],
        accept_multiple_files=True
    )

    if not uploaded_files:
        st.info("请上传音视频文件开始识别。系统支持自动生成 SRT、VTT、ASS 特效字幕及视频字幕硬烧录。")
        st.markdown("<div class='footer-text'>© 2026 Open Caption by YO JI STUDIO • Open Source Subtitle Studio</div>", unsafe_allow_html=True)
        return

    st.markdown(f"##### 待处理清单 ({len(uploaded_files)} 个文件)")
    file_info_cols = st.columns(min(len(uploaded_files), 4))
    for idx, f in enumerate(uploaded_files):
        with file_info_cols[idx % 4]:
            st.caption(f"📄 {f.name} ({f.size / (1024*1024):.1f} MB)")

    start_btn = st.button("开始生成字幕", use_container_width=True)

    if "results" not in st.session_state:
        st.session_state.results = {}

    if start_btn:
        st.session_state.results = {}

        try:
            with st.spinner(f"正在加载 Whisper 模型 ({model_name})..."):
                model = load_whisper_model(model_name, device, compute_type)
        except Exception as e:
            st.error(f"模型加载失败: {str(e)}")
            return

        overall_progress = st.progress(0, text="开始处理...")
        
        for file_idx, file_obj in enumerate(uploaded_files):
            file_name = file_obj.name
            st.markdown(f"--- \n### 正在识别 ({file_idx+1}/{len(uploaded_files)}): `{file_name}`")

            suffix = os.path.splitext(file_name)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                tmp_file.write(file_obj.read())
                tmp_file_path = tmp_file.name

            preview_container = st.empty()
            live_segments = []

            vad_params = dict(min_silence_duration_ms=min_silence_ms) if use_vad else None

            start_time = time.time()
            try:
                segments_generator, info = model.transcribe(
                    tmp_file_path,
                    task=task,
                    language=language_code,
                    vad_filter=use_vad,
                    vad_parameters=vad_params,
                    initial_prompt=initial_prompt if initial_prompt.strip() else None,
                    beam_size=5,
                    best_of=5,
                    word_timestamps=False
                )

                st.caption(f"语种: **{info.language}** (置信度: {info.language_probability:.2%}), 音频时长: {info.duration:.2f} s")

                for segment in segments_generator:
                    sub_texts = split_text_by_width(segment.text, max_width=max_line_width)
                    duration_per_part = (segment.end - segment.start) / max(len(sub_texts), 1)

                    for p_idx, sub_t in enumerate(sub_texts):
                        seg_start = segment.start + p_idx * duration_per_part
                        seg_end = seg_start + duration_per_part
                        
                        item = {
                            "start": seg_start,
                            "end": seg_end,
                            "text": sub_t
                        }
                        live_segments.append(item)
                    
                    progress_val = min(segment.end / info.duration, 1.0) if info.duration > 0 else 0.5
                    overall_progress.progress(
                        (file_idx + progress_val) / len(uploaded_files),
                        text=f"进度 [{file_name}]: {segment.end:.1f}s / {info.duration:.1f}s"
                    )

                    with preview_container.container():
                        st.markdown("""
                            <div class='stream-preview-card'>
                                <div style='font-size: 0.85rem; color: #989eba; font-weight: 500; margin-bottom: 8px;'>实时文本流预览</div>
                        """, unsafe_allow_html=True)
                        
                        recent_items = live_segments[-6:]
                        for r_item in recent_items:
                            st.markdown(
                                f"<div class='subtitle-row'>"
                                f"<div class='subtitle-time'>{format_timestamp(r_item['start'])} ➔ {format_timestamp(r_item['end'])}</div>"
                                f"<div class='subtitle-text'>{r_item['text']}</div>"
                                f"</div>",
                                unsafe_allow_html=True
                            )
                        st.markdown("</div>", unsafe_allow_html=True)

                elapsed = time.time() - start_time
                st.success(f"`{file_name}` 处理完成，耗时 {elapsed:.2f} 秒。")

                st.session_state.results[file_name] = {
                    "segments": live_segments,
                    "tmp_file_path": tmp_file_path,
                    "duration": info.duration,
                    "language": info.language
                }

            except Exception as ex:
                st.error(f"处理 `{file_name}` 时出错: {str(ex)}")

            overall_progress.progress((file_idx + 1) / len(uploaded_files))

        st.toast("所有文件识别完成！", icon="✅")
        clear_vram()

    # ===========================================================================
    # 6. 转写结果展示、在线编辑、格式导出与烧录
    # ===========================================================================
    if st.session_state.results:
        st.divider()
        st.markdown("## 字幕管理与后期工作室")

        target_file_name = st.selectbox(
            "选择要处理的目标文件",
            options=list(st.session_state.results.keys())
        )

        curr_data = st.session_state.results[target_file_name]
        raw_segments = curr_data["segments"]
        tmp_video_path = curr_data["tmp_file_path"]

        tab_edit, tab_export, tab_burn, tab_batch = st.tabs([
            "✏️ 字幕表格与批量替换",
            "📄 格式导出与复制",
            "🎬 视频硬字幕烧录",
            "📦 批量打包下载"
        ])

        # -----------------------------------------------------------------------
        # TAB 1: 在线字幕编辑与全局批量查找替换
        # -----------------------------------------------------------------------
        with tab_edit:
            st.markdown("##### 🔍 全局查找与批量替换")
            sc1, sc2, sc3 = st.columns([2, 2, 1])
            with sc1:
                search_term = st.text_input("查找文本", key="search_term", placeholder="如：旧词/错别字")
            with sc2:
                replace_term = st.text_input("替换为", key="replace_term", placeholder="如：新词/品牌名")
            with sc3:
                st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                do_replace = st.button("一键批量替换", use_container_width=True)

            if do_replace and search_term:
                replaced_count = 0
                for s in raw_segments:
                    if search_term in s["text"]:
                        s["text"] = s["text"].replace(search_term, replace_term)
                        replaced_count += 1
                st.toast(f"已成功批量替换 {replaced_count} 处匹配项！", icon="🎉")

            st.caption("双击下方表格直接修改文本或时间戳：")

            df_data = []
            for idx, s in enumerate(raw_segments):
                df_data.append({
                    "序号": idx + 1,
                    "开始时间": format_timestamp(s["start"], "srt"),
                    "结束时间": format_timestamp(s["end"], "srt"),
                    "字幕文本": s["text"]
                })

            df = pd.DataFrame(df_data)

            edited_df = st.data_editor(
                df,
                num_rows="dynamic",
                use_container_width=True,
                column_config={
                    "序号": st.column_config.NumberColumn("序号", disabled=True, width="small"),
                    "开始时间": st.column_config.TextColumn("开始时间", width="medium"),
                    "结束时间": st.column_config.TextColumn("结束时间", width="medium"),
                    "字幕文本": st.column_config.TextColumn("字幕文本", width="large")
                }
            )

            updated_segments = []
            def parse_time_to_seconds(t_str: str) -> float:
                try:
                    t_str = t_str.replace(",", ".")
                    parts = t_str.split(":")
                    h, m, s = float(parts[0]), float(parts[1]), float(parts[2])
                    return h * 3600 + m * 60 + s
                except Exception:
                    return 0.0

            for _, row in edited_df.iterrows():
                updated_segments.append({
                    "start": parse_time_to_seconds(str(row["开始时间"])),
                    "end": parse_time_to_seconds(str(row["结束时间"])),
                    "text": str(row["字幕文本"])
                })

        # -----------------------------------------------------------------------
        # TAB 2: 多格式导出与复制 (.SRT / .VTT / .ASS / PlainText)
        # -----------------------------------------------------------------------
        with tab_export:
            srt_content = generate_srt_content(updated_segments)
            vtt_content = generate_vtt_content(updated_segments)
            ass_content = generate_ass_content(updated_segments, title=f"Open Caption - {target_file_name}")
            plain_text_content = generate_plain_text(updated_segments)

            base_name = os.path.splitext(target_file_name)[0]

            btn_col1, btn_col2, btn_col3 = st.columns(3)
            with btn_col1:
                st.download_button(
                    label="⬇️ 下载 .SRT 标准字幕",
                    data=srt_content.encode("utf-8"),
                    file_name=f"{base_name}.srt",
                    mime="text/plain",
                    use_container_width=True
                )
            with btn_col2:
                st.download_button(
                    label="⬇️ 下载 .VTT Web 字幕",
                    data=vtt_content.encode("utf-8"),
                    file_name=f"{base_name}.vtt",
                    mime="text/vtt",
                    use_container_width=True
                )
            with btn_col3:
                st.download_button(
                    label="⬇️ 下载 .ASS 特效字幕 (Pr/FinalCut)",
                    data=ass_content.encode("utf-8"),
                    file_name=f"{base_name}.ass",
                    mime="text/plain",
                    use_container_width=True
                )

            st.divider()
            st.markdown("##### 纯文本结果 (无时间轴)")
            st.text_area("纯文本", value=plain_text_content, height=180)

        # -----------------------------------------------------------------------
        # TAB 3: 视频硬烧录 (支持 NVENC GPU 加速)
        # -----------------------------------------------------------------------
        with tab_burn:
            is_video = target_file_name.lower().endswith((".mp4", ".mkv", ".mov", ".avi", ".webm"))

            if not is_video:
                st.warning("所选文件为纯音频格式，无法进行视频硬字幕烧录。")
            elif not ffmpeg_ready:
                st.error("系统未准备好 FFmpeg 环境，无法烧录。")
            else:
                col_s1, col_s2, col_s3 = st.columns(3)
                with col_s1:
                    font_size = st.slider("字幕字号", 12, 40, 22)
                with col_s2:
                    font_color_choice = st.selectbox("文字颜色", ["白色", "黄色", "青色"])
                    color_map = {
                        "白色": "&H00FFFFFF",
                        "黄色": "&H0000FFFF",
                        "青色": "&H00FFFF00"
                    }
                with col_s3:
                    outline_color_choice = st.selectbox("描边颜色", ["黑色", "深灰色", "无"])
                    outline_map = {
                        "黑色": "&H00000000",
                        "深灰色": "&H00333333",
                        "无": "&HFF000000"
                    }

                use_gpu_burn = st.checkbox("开启 NVENC 显卡 GPU 烧录加速 (提升 5~10 倍合成速度)", value=is_nvenc_ready)

                if st.button("开始硬烧录视频", use_container_width=True):
                    with st.spinner("FFmpeg 正在硬烧录字幕..."):
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".srt", mode="w", encoding="utf-8") as tmp_srt:
                            tmp_srt.write(srt_content)
                            tmp_srt_path = tmp_srt.name

                        output_burned_video = os.path.join(tempfile.gettempdir(), f"burned_{base_name}.mp4")
                        
                        success, msg = burn_subtitles_to_video(
                            video_path=tmp_video_path,
                            srt_path=tmp_srt_path,
                            output_video_path=output_burned_video,
                            font_size=font_size,
                            font_color=color_map[font_color_choice],
                            outline_color=outline_map[outline_color_choice],
                            use_nvenc=use_gpu_burn
                        )

                        if success and os.path.exists(output_burned_video):
                            st.success("视频烧录成功！")
                            st.video(output_burned_video)
                            
                            with open(output_burned_video, "rb") as vf:
                                st.download_button(
                                    label="下载字幕版 MP4",
                                    data=vf.read(),
                                    file_name=f"{base_name}_字幕版.mp4",
                                    mime="video/mp4",
                                    use_container_width=True
                                )
                        else:
                            st.error(msg)

        # -----------------------------------------------------------------------
        # TAB 4: 批量打包导出
        # -----------------------------------------------------------------------
        with tab_batch:
            st.caption(f"共包含 {len(st.session_state.results)} 个文件的字幕。")

            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for fname, res in st.session_state.results.items():
                    bname = os.path.splitext(fname)[0]
                    segs = res["segments"]
                    
                    srt_data = generate_srt_content(segs)
                    zip_file.writestr(f"{bname}.srt", srt_data)
                    
                    vtt_data = generate_vtt_content(segs)
                    zip_file.writestr(f"{bname}.vtt", vtt_data)

                    ass_data = generate_ass_content(segs, title=f"Open Caption - {bname}")
                    zip_file.writestr(f"{bname}.ass", ass_data)

                    txt_data = generate_plain_text(segs)
                    zip_file.writestr(f"{bname}.txt", txt_data)

            zip_buffer.seek(0)

            st.download_button(
                label="下载全部字幕打包 (.ZIP)",
                data=zip_buffer,
                file_name="Open_Caption_Subtitles.zip",
                mime="application/zip",
                use_container_width=True
            )

    st.markdown("<div class='footer-text'>© 2026 Open Caption by YO JI STUDIO • Open Source Subtitle Studio</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
