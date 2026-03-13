@echo off
chcp 65001 >nul
echo ========================================
echo   PMS 生产管理系统 - 前端服务启动
echo ========================================
echo.

cd /d "%~dp0frontend"

echo [1/2] 检查 Node.js 环境...
node --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Node.js，请先安装 Node.js 18+
    pause
    exit /b 1
)
echo [OK] Node.js 环境正常

echo.
echo [2/2] 安装依赖并启动开发服务...
npm install
echo.
echo ========================================
echo   前端服务已启动!
echo   访问：http://localhost:3000
echo ========================================
echo.
echo 按 Ctrl+C 停止服务
echo.

npm run dev
