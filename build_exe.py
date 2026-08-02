# -*- coding: utf-8 -*-
"""
Open Caption by YO JI STUDIO - PyInstaller EXE 自动化打包脚本
使用方式: python build_exe.py
"""

import os
import sys
import subprocess

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    print("===================================================================")
    print("      Open Caption by YO JI STUDIO - EXE 打包构建工具")
    print("===================================================================")

    # 确认安装 PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print("正在安装 PyInstaller 打包依赖...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=Open_Caption_Studio",
        "--onedir",
        "--noconsole",
        "--add-data=app.py;.",
        "--add-data=.streamlit;.streamlit",
        "--add-data=logo.png;.",
        "desktop_app.py"
    ]

    print("正在编译封装为可执行桌面应用包...")
    result = subprocess.call(cmd)

    if result == 0:
        print("\n🎉 构建成功！输出目录为: dist/Open_Caption_Studio")
        print("直接运行 dist/Open_Caption_Studio/Open_Caption_Studio.exe 即可启动桌面应用！")
    else:
        print("\n❌ 构建失败，请检查编译输出日志。")

if __name__ == "__main__":
    main()
