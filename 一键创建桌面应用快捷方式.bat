@echo off
chcp 65001 >nul
title 创建桌面应用快捷方式...

cd /d "%~dp0"

powershell -NoProfile -ExecutionPolicy Bypass -Command "$ws = New-Object -ComObject WScript.Shell; $d = [Environment]::GetFolderPath('Desktop'); $lnk = [System.IO.Path]::Combine($d, 'Open Caption by YO JI STUDIO.lnk'); $s = $ws.CreateShortcut($lnk); $s.TargetPath = [System.IO.Path]::Combine('%~dp0', '启动软件.bat'); $s.WorkingDirectory = '%~dp0'; if (Test-Path '%~dp0logo.png') { $s.IconLocation = '%~dp0logo.png' }; $s.Save()"

echo.
echo ===============================================================================
echo   🎉 桌面快捷方式生成成功！
echo   已在您的 Windows 桌面上生成「Open Caption by YO JI STUDIO」图标。
echo   以后双击桌面图标即可直接启动应用！
echo ===============================================================================
echo.
pause
