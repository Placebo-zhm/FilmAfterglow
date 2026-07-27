# 摄影个人主页后端开发文档（初版）

> 版本：v0.1  
> 目标：完成摄影个人主页后端的基础能力，支持胶片摄影、数码摄影、管理员登录鉴权和图片管理。

---

## 1. 项目范围

后端第一版需要实现：

- 管理员登录与鉴权；
- 游客或普通用户查看已发布内容；
- 管理员维护摄影师个人信息；
- 管理员创建、修改、删除摄影系列；
- 管理员上传、修改、排序和删除图片；
- 支持胶片摄影和数码摄影；
- 支持整组上传和单张追加上传；
- 支持系列默认地点和单张图片地点；
- 支持草稿、发布和归档状态；
- 支持图片封面、排序和软删除。

第一版暂不包含：

- 评论；
- 收藏；
- 关注；
- 图片购买；
- 多摄影师入驻；
- 多管理员协作。

---

## 2. 用户角色与权限

| 角色 | 权限 |
|---|---|
| 游客 | 查看已发布且公开的个人资料、摄影系列和图片 |
| 普通用户 | 第一版与游客相同，预留后续收藏、评论能力 |
| 管理员 | 管理个人资料、摄影系列、图片、地点和胶卷型号 |

如果普通用户只有查看权限，第一版可暂不实现普通用户注册，只保留游客和管理员。

---

## 3. 核心设计

胶片摄影和数码摄影统一使用“摄影系列”模型，不分别设计两套图片系统。

```text
PhotoSeries
├── type = film
└── type = digital
```

一卷胶片对应一个胶片摄影系列。

一组数码照片对应一个数码摄影系列。

两类系列共用：

- 标题；
- 描述；
- 封面；
- 拍摄日期；
- 默认地点；
- 图片列表；
- 图片排序；
- 发布状态。

胶片摄影额外保存胶卷相关信息。

---

## 4. 核心数据模型

### 4.1 User

管理员账号。

主要字段：

```text
id
username
password_hash
role
is_active
created_at
updated_at
```

---

### 4.2 Profile

摄影师个人资料，建议作为单例资源。

主要字段：

```text
id
display_name
avatar_url
cover_url
bio
email
website
location_text
equipment
created_at
updated_at
```

---

### 4.3 PhotoSeries

统一表示胶片卷和数码编组。

主要字段：

```text
id
title
slug
type                 # film / digital
description
cover_photo_id
default_location_id
shot_date
status               # draft / published / archived
visibility           # public / private
sort_order
published_at
created_at
updated_at
deleted_at
```

关键规则：

- 只有 `published + public` 的系列可公开访问；
- 封面图片必须属于当前系列；
- 删除系列默认使用软删除；
- `type=film` 时关联胶片信息。

---

### 4.4 FilmStock

胶卷型号字典，避免重复输入。

主要字段：

```text
id
brand
name
iso
format
process
```

示例：

```text
Kodak / Portra 400 / ISO 400 / 135 / C-41
```

---

### 4.5 FilmInfo

胶片摄影系列的附加信息。

主要字段：

```text
id
series_id
film_stock_id
roll_number
development_lab
scanner
expired_at
notes
```

---

### 4.6 Photo

图片信息。

主要字段：

```text
id
series_id
original_filename
storage_key
preview_key
thumbnail_key
mime_type
file_size
width
height
checksum
caption
alt_text
location_id
shot_at
sort_order
status
exif_data
created_at
updated_at
deleted_at
```

图片状态：

```text
processing
ready
failed
hidden
```

---

### 4.7 Location

地点信息。

主要字段：

```text
id
country
province
city
district
name
latitude
longitude
```

地点规则：

```text
图片有效地点 = 图片地点 或 系列默认地点
```

---

## 5. 胶片摄影流程

### 5.1 整卷上传

1. 创建胶片摄影系列；
2. 选择胶卷型号；
3. 填写胶卷编号等信息；
4. 设置整卷默认地点；
5. 批量上传图片；
6. 单独修改部分图片地点；
7. 调整图片顺序；
8. 设置封面；
9. 发布系列。

### 5.2 单张追加

单张胶片图片必须：

- 添加到已有胶片系列；
- 或先创建一个新的胶片系列。

不允许存在没有所属胶卷的胶片图片。

---

## 6. 数码摄影流程

1. 创建数码摄影系列；
2. 填写标题、描述和拍摄日期；
3. 设置默认地点；
4. 单张或批量上传图片；
5. 自动提取拍摄时间和 EXIF；
6. 调整图片地点和顺序；
7. 设置封面；
8. 发布系列。

数码摄影不需要胶卷型号、冲洗店和扫描设备等信息。

---

## 7. 图片上传与存储

图片文件不直接存入数据库。

推荐：

```text
数据库：
保存图片元数据、地点、排序、状态和对象存储地址

对象存储：
保存原图、预览图和缩略图
```

建议保存三种规格：

```text
original
preview
thumbnail
```

上传后需要处理：

- 校验真实文件类型；
- 校验文件大小；
- 计算文件哈希；
- 检查重复文件；
- 自动修正图片方向；
- 提取宽高和 EXIF；
- 生成预览图；
- 生成缩略图；
- 更新处理状态。

批量上传应允许部分成功，不因一张图片失败导致全部失败。

---

## 8. 图片管理功能

管理员需要支持：

- 单张上传；
- 批量上传；
- 修改图片说明；
- 修改单张图片地点；
- 批量修改地点；
- 调整图片顺序；
- 设置系列封面；
- 移动图片到其他系列；
- 隐藏图片；
- 单张删除；
- 批量删除；
- 恢复软删除图片；
- 查看上传失败原因。

---

## 9. 删除规则

系列和图片默认使用软删除：

```text
deleted_at = 当前时间
```

软删除后：

- 前台不可见；
- 管理列表默认不显示；
- 回收站可查看和恢复；
- 对象存储文件暂不删除。

后续可通过定时任务清理超过保留期的图片文件。

---

## 10. 鉴权设计

建议使用：

- Access Token；
- Refresh Token；
- JWT；
- Argon2 或 bcrypt 密码加密。

核心接口：

```http
POST /api/auth/login
POST /api/auth/refresh
POST /api/auth/logout
GET  /api/auth/me
POST /api/auth/change-password
```

安全要求：

- 管理接口必须校验管理员角色；
- 登录接口需要限流；
- Token 失效后不可继续访问；
- 生产环境使用 HTTPS；
- CORS 使用白名单；
- 上传文件必须校验真实类型。

---

## 11. 核心 API

### 11.1 个人资料

```http
GET   /api/profile
PATCH /api/admin/profile
```

### 11.2 公开摄影系列

```http
GET /api/series
GET /api/series/{slug}
```

### 11.3 管理摄影系列

```http
POST   /api/admin/series
GET    /api/admin/series
GET    /api/admin/series/{id}
PATCH  /api/admin/series/{id}
DELETE /api/admin/series/{id}
POST   /api/admin/series/{id}/restore
```

### 11.4 图片管理

```http
POST   /api/admin/series/{id}/photos
GET    /api/admin/photos/{id}
PATCH  /api/admin/photos/{id}
DELETE /api/admin/photos/{id}
POST   /api/admin/photos/{id}/restore
```

### 11.5 图片批量操作

```http
PATCH  /api/admin/photos/batch-location
PATCH  /api/admin/photos/reorder
POST   /api/admin/photos/move
DELETE /api/admin/photos/batch
```

### 11.6 封面

```http
PATCH /api/admin/series/{id}/cover
```

### 11.7 地点和胶卷型号

```http
GET    /api/admin/locations
POST   /api/admin/locations
PATCH  /api/admin/locations/{id}
DELETE /api/admin/locations/{id}

GET    /api/admin/film-stocks
POST   /api/admin/film-stocks
PATCH  /api/admin/film-stocks/{id}
DELETE /api/admin/film-stocks/{id}
```

---

## 12. 第一版开发优先级

### P0：必须完成

- 管理员登录；
- JWT 鉴权；
- 个人资料读取和修改；
- 摄影系列统一模型；
- 胶片信息；
- 胶卷型号；
- 单张和批量图片上传；
- 对象存储；
- 图片预览图和缩略图；
- 系列默认地点；
- 单图地点覆盖；
- 图片排序；
- 设置封面；
- 草稿和发布；
- 软删除；
- 公开系列列表和详情。

### P1：建议完成

- Refresh Token；
- 图片移动；
- 批量修改地点；
- 批量删除；
- 删除恢复；
- EXIF 提取；
- 重复文件检测；
- 管理员操作日志。

### P2：后续扩展

- 标签；
- 地图；
- 搜索；
- 普通用户注册；
- 收藏；
- 评论；
- AI 自动分类；
- 多管理员。

---

## 13. 第一版验收标准

后端第一版至少满足：

- 管理员能够登录和访问管理接口；
- 游客无法访问管理接口；
- 管理员可修改个人资料；
- 管理员可创建胶片和数码摄影系列；
- 胶片系列可选择胶卷型号；
- 可单张和批量上传图片；
- 可设置系列默认地点；
- 可单独修改图片地点；
- 可调整图片顺序；
- 可设置封面；
- 可发布、归档、删除和恢复系列；
- 图片存储在对象存储中；
- 批量上传支持部分成功；
- 游客只能查看已发布且公开的内容；
- 图片地点可正确继承系列默认地点。

---

## 14. 待确认事项

正式开发前需要确定：

1. 第一版是否需要普通用户登录；
2. 是否需要私密摄影系列；
3. 是否允许下载原图；
4. 是否公开 EXIF；
5. 是否公开精确 GPS；
6. 支持哪些图片格式；
7. 单张图片最大大小；
8. 单次最大上传数量；
9. 软删除保留时间；
10. 对象存储使用 MinIO 还是云存储。

---

## 15. 初版结论

第一版围绕以下四个模型开发：

```text
PhotoSeries
Photo
FilmInfo
Location
```

重点解决：

- 图片从上传到展示的完整流程；
- 摄影系列从草稿到发布的流程；
- 系列默认地点与单图地点覆盖；
- 数据库记录与对象存储文件的一致性。
