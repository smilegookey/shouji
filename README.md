# shouji
sms接码平台

## 后端启动

1. 安装依赖

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell 启动虚拟环境：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Windows CMD 启动虚拟环境：

```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
pip install -r requirements.txt
```

2. 配置环境变量

```bash
cp .env.example .env
```

3. 启动服务

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 前端启动

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## 管理员账号

后端启动时会读取 `.env` 中的 `ADMIN_EMAIL` 与 `ADMIN_PASSWORD`，如果不存在会自动创建管理员账号。
