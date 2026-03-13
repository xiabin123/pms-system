# PMS 生产管理系统 - 部署指南

## 🌐 部署到公网让别人访问

你的项目是前后端分离架构，需要分别部署。以下是几种方案：

---

## 方案一：Railway 部署（推荐⭐ 免费 + 长期）

Railway 提供免费额度，适合展示和长期使用。

### 步骤 1：准备 GitHub 仓库

```powershell
# 进入项目目录
cd D:\qt\pms-system

# 初始化 git（如果还没有）
git init
git add .
git commit -m "Initial commit"
```

### 步骤 2：创建 GitHub 仓库

1. 访问 https://github.com/new
2. 创建新仓库，例如 `pms-system`
3. 按照提示推送代码：

```powershell
git remote add origin https://github.com/你的用户名/pms-system.git
git branch -M main
git push -u origin main
```

### 步骤 3：部署到 Railway

1. 访问 https://railway.app
2. 注册/登录账号
3. 点击 "New Project" → "Deploy from GitHub repo"
4. 选择你的 `pms-system` 仓库

### 步骤 4：配置 Railway

Railway 需要分别部署前端和后端：

#### 后端配置（backend）

在 Railway 项目设置中：
- **Root Directory**: `backend`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **环境变量**: 无需特殊配置

#### 前端配置（frontend）

新建一个服务：
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Start Command**: `npm run preview -- --host 0.0.0.0 --port $PORT`

### 步骤 5：获取公网 URL

部署完成后，Railway 会给你两个 URL：
- 后端：`https://pms-backend-production.up.railway.app`
- 前端：`https://pms-frontend-production.up.railway.app`

### ⚠️ 重要：修改前端 API 地址

部署后需要修改前端的 API 基础 URL：

编辑 `frontend/src/api/index.js`（或类似文件），将：
```javascript
const BASE_URL = 'http://localhost:8000'
```
改为：
```javascript
const BASE_URL = 'https://你的后端地址.up.railway.app'
```

然后重新构建并推送。

---

## 方案二：Vercel + Railway 组合（最佳实践）

- **前端**: 部署到 Vercel（完全免费，CDN 加速）
- **后端**: 部署到 Railway

### 前端部署到 Vercel

1. 访问 https://vercel.com
2. 登录（可用 GitHub 账号）
3. "Add New" → "Project"
4. 选择你的 GitHub 仓库
5. 配置：
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
6. 点击 Deploy

### 后端部署到 Railway

同上方案一。

---

## 方案三：ngrok 快速暴露（临时演示）

适合临时给别人展示，5 分钟搞定。

### 步骤 1：启动本地服务

```powershell
# 终端 1 - 启动后端
cd D:\qt\pms-system\backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000

# 终端 2 - 启动前端
cd D:\qt\pms-system\frontend
npm run dev
```

### 步骤 2：下载 ngrok

访问 https://ngrok.com/download
或使用 Chocolatey 安装：
```powershell
choco install ngrok
```

### 步骤 3：创建隧道

```powershell
# 暴露后端
ngrok http 8000

# 新窗口 - 暴露前端
ngrok http 3000
```

### 步骤 4：获取临时 URL

ngrok 会给你两个临时 URL：
- `https://xxx-xxx.ngrok.io` (后端)
- `https://yyy-yyy.ngrok.io` (前端)

**注意**: ngrok 免费版每次重启 URL 会变，且连接数有限制。

---

## 方案四：Cloudflare Tunnel（免费 + 稳定）

### 步骤 1：安装 cloudflared

```powershell
winget install Cloudflare.cloudflared
```

### 步骤 2：登录 Cloudflare

```powershell
cloudflared tunnel login
```

### 步骤 3：创建隧道

```powershell
cloudflared tunnel create pms-tunnel
cloudflared tunnel route dns pms-tunnel pms.yourdomain.com
```

### 步骤 4：运行隧道

```powershell
cloudflared tunnel run pms-tunnel --url http://localhost:3000
```

---

## 📋 部署后检查清单

- [ ] 后端 API 可访问
- [ ] 前端页面可访问
- [ ] 前端能正确调用后端 API（CORS 配置）
- [ ] 登录功能正常
- [ ] 数据库数据持久化
- [ ] 静态资源加载正常

---

## 🔧 生产环境优化建议

### 1. 数据库迁移

SQLite 不适合生产，建议迁移到 PostgreSQL：

```python
# requirements.txt 添加
psycopg2-binary
```

### 2. 添加认证

当前是简单密码验证，建议添加 JWT：

```python
# backend/requirements.txt 添加
python-jose[cryptography]
passlib[bcrypt]
```

### 3. 环境变量配置

创建 `.env` 文件：
```env
DATABASE_URL=postgresql://user:pass@host:5432/pms
SECRET_KEY=your-secret-key
FRONTEND_URL=https://your-frontend.vercel.app
```

---

## 🚀 快速开始（推荐新手）

**最简单的方式**：使用 **Render.com**

1. 访问 https://render.com
2. 注册账号
3. "New +" → "Web Service"
4. 连接 GitHub 仓库
5. 选择 `backend` 目录
6. 自动部署！

Render 提供免费层，适合小型项目展示。

---

## 💡 需要帮助？

告诉我你想用哪个方案，我可以帮你：
- 自动配置 GitHub 仓库
- 生成部署脚本
- 修改代码适配生产环境
- 配置域名和 HTTPS
