# GitHub 推送失败 - 替代方案

由于国内网络原因，GitHub 连接超时。请用以下方法之一推送代码：

---

## 方法 1：使用 GitHub Desktop（推荐⭐ 最简单）

### 下载
访问：https://desktop.github.com/download/

### 使用步骤
1. 安装 GitHub Desktop
2. 登录你的 GitHub 账号（xiabin123）
3. 点击 **File** → **Add Local Repository**
4. 选择文件夹：`D:\qt\pms-system`
5. 会提示你初始化或添加，选择 **Add Repository**
6. 点击右上角 **Publish repository**
7. 名称填 `pms-system`，勾选 **Keep this code private**（如果需要）
8. 点击 **Publish Repository**

完成！代码就上传到 GitHub 了。

---

## 方法 2：使用 Gitee（码云）中转

如果 GitHub 实在连不上，可以先用国内的 Gitee：

### 1. 访问 Gitee
https://gitee.com

### 2. 创建仓库
- 用户名：xiabin123
- 仓库名：pms-system
- 设为公开

### 3. 推送命令
```powershell
cd D:\qt\pms-system
git remote add origin https://gitee.com/xiabin123/pms-system.git
git push -u origin main
```

### 4. 从 Gitee 同步到 GitHub
在 Gitee 仓库设置里配置 **同步到 GitHub**

---

## 方法 3：手动上传（不推荐）

1. 访问：https://github.com/xiabin123/pms-system
2. 点击 **uploading an existing file**
3. 拖拽文件上传
4. 但这样会丢失 git 历史，不推荐

---

## 推送完成后

代码上传到 GitHub 后，告诉我，我帮你配置 Railway 部署！

部署地址：https://railway.app

---

## 检查是否推送成功

访问：https://github.com/xiabin123/pms-system

如果能看到你的代码，就说明成功了！
