@echo off
chcp 65001 >nul
echo ========================================
echo   PMS 生产管理系统 - 后端服务启动
echo ========================================
echo.

cd /d "%~dp0backend"

echo [1/2] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.10+
    pause
    exit /b 1
)
echo [OK] Python 环境正常

echo.
echo [2/2] 安装依赖并启动服务...
pip install -r requirements.txt -q
echo.
echo ========================================
echo   后端服务已启动!
echo   API: http://localhost:8000
echo   文档：http://localhost:8000/docs
echo ========================================
echo.
echo 按 Ctrl+C 停止服务
echo.

python main.py
