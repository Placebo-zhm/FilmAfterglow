# FilmAfterglow Backend

FilmAfterglow 的 FastAPI 后端项目。

## 本地运行

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
uvicorn app.main:app --reload
```

启动后可以访问：

- API 文档：http://127.0.0.1:8000/docs
- 健康检查：http://127.0.0.1:8000/api/v1/health

## 项目结构

```text
backend/
├── app/
│   ├── api/
│   │   ├── public/
│   │   └── admin/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── storage/
│   ├── tasks/
│   ├── utils/
│   └── main.py
├── alembic/
├── tests/
├── scripts/
├── uploads/
├── .env.example
└── pyproject.toml
```

## 目录用途

- `app/`：后端主要代码。
- `app/api/`：接口路由及路由聚合。
- `app/api/public/`：公开访问接口，例如影片展示、搜索和健康检查。
- `app/api/admin/`：需要管理员身份才能访问的管理接口。
- `app/core/`：配置、安全、异常处理、日志等基础能力。
- `app/db/`：数据库连接、会话管理和初始化逻辑。
- `app/models/`：数据库 ORM 模型。
- `app/schemas/`：请求参数和响应数据结构。
- `app/services/`：业务逻辑，避免在路由中堆积业务代码。
- `app/storage/`：本地文件存储或对象存储操作。
- `app/tasks/`：图片处理等后台任务。
- `app/utils/`：无业务状态的通用工具函数。
- `alembic/`：数据库迁移脚本和 Alembic 配置。
- `tests/`：自动化测试。
- `scripts/`：初始化管理员、数据导入及数据修复等一次性脚本。
- `uploads/`：本地开发时的临时图片目录；实际上传文件不会提交到 Git。

## 路由约定

- 公开接口：`/api/v1/...`
- 管理接口：`/api/v1/admin/...`

新增接口时，在对应的 `public` 或 `admin` 目录创建路由模块，再在该目录的
`router.py` 中注册。路由只负责参数接收和响应转换，核心业务逻辑放入
`app/services/`。

## 环境配置

复制 `.env.example` 为 `.env` 后按需修改。所有环境变量均使用
`FILMAFTERGLOW_` 前缀，避免与操作系统或其他项目的变量冲突。

例如：

```dotenv
FILMAFTERGLOW_DEBUG=true
FILMAFTERGLOW_CORS_ORIGINS=["http://localhost:5173"]
```

## 测试与代码检查

```powershell
pytest
ruff check app tests
```
