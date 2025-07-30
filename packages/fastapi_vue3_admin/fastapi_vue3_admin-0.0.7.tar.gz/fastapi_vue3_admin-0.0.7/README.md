# fastapi_vue3_admin

FastAPI + Vue3 的現代化管理後台腳手架。 

## 快速開始

### 後端
```bash
poetry install --no-root
poetry run fastapi_vue3_admin dev
```

### 前端
```bash
cd frontend
npm install
npm run dev
```

### 資料庫遷移 (Alembic)
```bash
poetry run fastapi_vue3_admin migrate -m "init"
```

### Docker
```bash
# 建立映像並啟動（含 Postgres）
docker-compose up --build
```

### 生成新專案腳手架
```bash
# 安裝套件後
fva create my_project
```

啟動後：
- API: http://localhost:8000/docs
- DB:  postgres://fastapi:fastapi@localhost:5432/fastapi_db 