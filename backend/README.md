# FilmAfterglow Backend

FilmAfterglow 是一个面向摄影师的个人作品展示与管理平台。本仓库中的
`backend` 是平台的 FastAPI 后端服务。

## 项目简介

平台用于展示摄影师的个人资料、胶片摄影作品和数码摄影作品，分为公开展示端与
后台管理端：

- 游客可以浏览已发布的摄影作品和摄影师个人资料。
- 管理员登录后可以维护个人信息、上传和管理图片、设置拍摄地点、调整图片顺序，
  并控制作品的发布状态。

胶片摄影与数码摄影均支持单张上传和批量上传。每张图片既可以作为独立作品存在，
也可以按需归属于胶卷或摄影编组，不强制关联分组。

- 胶片摄影可以额外记录胶卷型号、胶卷编号等信息，并通过胶卷组织作品。
- 数码摄影可以通过摄影编组整理同一主题、地点或时间段的作品。

后端负责管理员登录鉴权、作品及个人资料管理、图片上传、对象存储等功能，并为
前端提供统一的 RESTful API。业务数据使用 MongoDB 存储，异步数据库访问基于
PyMongo Async API。

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
- `app/api/public/`：游客可访问的公开展示接口。
- `app/api/admin/`：需要管理员身份才能访问的管理接口。
- `app/core/`：配置、安全、异常处理、日志等基础能力。
- `app/db/`：MongoDB 异步客户端、连接生命周期和数据库依赖。
- `app/models/`：MongoDB 文档模型及集合定义。
- `app/schemas/`：请求参数和响应数据结构。
- `app/services/`：平台业务逻辑。
- `app/storage/`：本地文件存储或对象存储操作。
- `app/tasks/`：图片处理等后台任务。
- `app/utils/`：无业务状态的通用工具函数。
- `alembic/`：当前不使用。Alembic 面向关系型数据库，MongoDB 数据变更脚本放在
  `scripts/` 中管理。
- `tests/`：自动化测试。
- `scripts/`：初始化管理员、数据导入及数据修复等一次性脚本。
- `uploads/`：本地开发时的临时图片目录；实际上传文件不会提交到 Git。

## 路由约定

- 公开接口：`/api/v1/...`
- 管理接口：`/api/v1/admin/...`

新增接口时，在对应的 `public` 或 `admin` 目录创建路由模块，再在该目录的
`router.py` 中注册。路由负责参数接收和响应转换，核心业务逻辑放入
`app/services/`。

## 环境配置

复制 `.env.example` 为 `.env` 后按需修改。所有环境变量均使用
`FILMAFTERGLOW_` 前缀，避免与操作系统或其他项目的变量冲突。

例如：

```dotenv
FILMAFTERGLOW_DEBUG=true
FILMAFTERGLOW_CORS_ORIGINS=["http://localhost:5173"]
FILMAFTERGLOW_MONGODB_URI=mongodb://localhost:27017
FILMAFTERGLOW_MONGODB_DATABASE=filmafterglow
```

应用启动时会连接 MongoDB 并执行 `ping`。连接失败时服务会停止启动，以避免在
数据库不可用的情况下继续接收业务请求。应用关闭时会自动释放 MongoDB 连接池。

## 测试与代码检查

```powershell
pytest
ruff check app tests
```
