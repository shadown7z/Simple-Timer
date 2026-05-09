@echo off
chcp 65001 >nul
title CountTime 计时器

echo ========================================
echo        CountTime 计时器启动中...
echo ========================================
echo.

:: 优先使用编译好的 exe 启动
if exist "dist\CountTime.exe" (
    echo [信息] 检测到编译版本，正在启动...
    start "" "dist\CountTime.exe"
    if %errorlevel% equ 0 (
        echo [成功] 计时器已启动
        goto :end
    )
)

:: exe 不存在或启动失败，回退到 Python 脚本
echo [信息] 未检测到编译版本，尝试 Python 脚本启动...

:: 检查 Python 是否可用
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 Python，请确保 Python 已安装并添加到 PATH
    pause
    exit /b 1
)

:: 检查 PyQt5 是否安装
python -c "import PyQt5" >nul 2>&1
if %errorlevel% neq 0 (
    echo [提示] 正在安装 PyQt5 依赖...
    pip install PyQt5 -q
    if %errorlevel% neq 0 (
        echo [错误] PyQt5 安装失败，请手动执行: pip install PyQt5
        pause
        exit /b 1
    )
    echo [成功] PyQt5 安装完成
)

:: 启动计时器
echo [信息] 正在启动计时器...
start "" python main.py
if %errorlevel% equ 0 (
    echo [成功] 计时器已启动
) else (
    echo [错误] 启动失败，请检查 main.py 是否存在
    pause
    exit /b 1
)

:end
echo.
echo 提示: 关闭计时器窗口即可退出程序
timeout /t 3 /nobreak >nul
