# GradientLab - CSS 渐变生成与预览工具

一个功能完整的 CSS 渐变生成器，支持用户注册、方案管理、公共分享和收藏功能。

## 项目简介

GradientLab 是一个基于 Vue3 + Flask 的前后端分离项目，提供直观的可视化界面来创建和管理 CSS 渐变方案。用户可以实时预览渐变效果，保存个人方案，并在公共广场分享和收藏他人的作品。

### 主要特性

- 🎨 **可视化编辑器**：圆盘式角度选择器、色标拖拽、实时预览
- 🔐 **用户系统**：JWT 认证、注册登录、个人方案管理
- 🌐 **公共广场**：分享作品、浏览社区创作、收藏喜欢的方案
- 📱 **响应式设计**：支持桌面端和移动端访问
- 🐳 **容器化部署**：Docker Compose 一键启动
- 💾 **数据持久化**：OpenGauss 数据库存储

## 技术栈

### 前端
- **框架**: Vue 3 (Composition API)
- **构建工具**: Vite
- **状态管理**: Pinia
- **路由**: Vue Router 4
- **HTTP 客户端**: Axios
- **样式**: 原生 CSS（深色主题）

### 后端
- **框架**: Flask 3.x
- **数据库**: OpenGauss / PostgreSQL
- **认证**: JWT (PyJWT)
- **密码加密**: bcrypt
- **数据库连接**: psycopg2

### 部署
- **容器化**: Docker + Docker Compose
- **Web 服务器**: Nginx (前端静态文件 + 反向代理)
- **多阶段构建**: 优化镜像大小

## 快速开始

### 前置要求

- Docker 20.10+
- Docker Compose 2.0+

### 一键启动

1. **克隆项目**

```bash
git clone <repository-url>
cd Frontend-Tool
```

2. **启动所有服务**

```bash
docker-compose up --build
```
重启前端:
```
docker-compose up -d --build frontend
```

首次启动需要构建镜像，大约需要 3-5 分钟。

3. **访问应用**

打开浏览器访问：`http://localhost`

### 服务端口

| 服务 | 端口 | 说明 |
|------|------|------|
| 前端 | 80 | 主要访问入口 |
| 后端 API | 5000 | RESTful API |
| 数据库 | 5432 | OpenGauss |

## 使用指南

### 1. 注册账号

- 访问 `http://localhost`
- 点击右上角"注册"按钮
- 输入用户名（3-20位字母数字）和密码（至少6位）

### 2. 创建渐变

- 登录后自动跳转到编辑器
- 选择渐变类型（线性/径向）
- 调整角度（仅线性渐变）
- 添加和编辑色标
- 实时预览效果

### 3. 保存方案

- 输入方案名称
- 选择是否公开到广场
- 点击"保存方案"

### 4. 分享与收藏

- 访问"公共广场"浏览所有公开方案
- 点击❤️收藏喜欢的作品
- 在"我的收藏"查看收藏列表

## 项目结构

```
Frontend-Tool/
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── database/          # 数据库连接池
│   │   ├── middleware/        # 认证中间件
│   │   ├── models/            # 数据模型
│   │   ├── routes/            # API 路由
│   │   ├── services/          # 业务逻辑
│   │   ├── __init__.py        # Flask 应用工厂
│   │   └── config.py          # 配置管理
│   ├── Dockerfile
│   ├── requirements.txt
│   └── run.py                 # 启动入口
│
├── frontend/                   # 前端应用
│   ├── src/
│   │   ├── api/               # API 接口封装
│   │   ├── components/        # Vue 组件
│   │   ├── router/            # 路由配置
│   │   ├── stores/            # Pinia 状态管理
│   │   ├── views/             # 页面组件
│   │   ├── App.vue
│   │   └── main.js
│   ├── Dockerfile
│   ├── nginx.conf             # Nginx 配置
│   ├── package.json
│   └── vite.config.js
│
├── docker-compose.yml          # Docker Compose 配置
├── init.sql                    # 数据库初始化脚本
└── README.md
```

## API 文档

### 认证接口

#### 注册
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "user123",
  "password": "password123"
}
```

#### 登录
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "user123",
  "password": "password123"
}
```

#### 获取当前用户信息
```http
GET /api/auth/me
Authorization: Bearer <token>
```

### 渐变方案接口

#### 获取我的方案
```http
GET /api/gradients/my
Authorization: Bearer <token>
```

#### 创建方案
```http
POST /api/gradients
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "我的渐变",
  "type": "linear",
  "angle": 90,
  "stops": [
    {"color": "#ff6b6b", "position": 0},
    {"color": "#4ecdc4", "position": 100}
  ],
  "css_value": "linear-gradient(90deg, #ff6b6b 0%, #4ecdc4 100%)",
  "is_public": true
}
```

#### 更新方案
```http
PUT /api/gradients/<id>
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "新名称",
  "is_public": false
}
```

#### 删除方案
```http
DELETE /api/gradients/<id>
Authorization: Bearer <token>
```

### 公共广场接口

#### 获取所有公开方案
```http
GET /api/plaza
```

### 收藏接口

#### 获取我的收藏
```http
GET /api/favorites
Authorization: Bearer <token>
```

#### 收藏方案
```http
POST /api/favorites/<gradient_id>
Authorization: Bearer <token>
```

#### 取消收藏
```http
DELETE /api/favorites/<gradient_id>
Authorization: Bearer <token>
```

## 开发指南

### 本地开发（不使用 Docker）

#### 后端开发

1. 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

2. 配置环境变量
```bash
export DATABASE_HOST=localhost
export DATABASE_PORT=5432
export DATABASE_NAME=postgres
export DATABASE_USER=gaussdb
export DATABASE_PASSWORD=OpenGauss@2024
export JWT_SECRET=your-secret-key
export FLASK_ENV=development
```

3. 启动后端
```bash
python run.py
```

#### 前端开发

1. 安装依赖
```bash
cd frontend
npm install
```

2. 启动开发服务器
```bash
npm run dev
```

3. 访问 `http://localhost:5173`

### 数据库管理

#### 连接数据库
```bash
docker exec -it gradient-db gsql -U gaussdb -d postgres
```

#### 查看表结构
```sql
\dt                    -- 列出所有表
\d users              -- 查看 users 表结构
\d gradients          -- 查看 gradients 表结构
\d favorites          -- 查看 favorites 表结构
```

#### 查询数据
```sql
SELECT * FROM users;
SELECT * FROM gradients WHERE is_public = true;
SELECT * FROM favorites;
```

## Docker 命令参考

### 基本操作

```bash
# 启动服务（前台运行）
docker-compose up

# 启动服务（后台运行）
docker-compose up -d

# 重新构建并启动
docker-compose up --build

# 停止服务
docker-compose down

# 停止服务并删除数据卷（重置数据库）
docker-compose down -v

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 查看特定服务的日志
docker-compose logs -f frontend
docker-compose logs -f backend
docker-compose logs -f opengauss
```

### 进入容器

```bash
# 进入前端容器
docker exec -it gradient-frontend sh

# 进入后端容器
docker exec -it gradient-backend sh

# 进入数据库容器
docker exec -it gradient-db bash
```

## 常见问题

### 1. 端口被占用

如果 80 端口被占用，可以修改 `docker-compose.yml` 中的端口映射：

```yaml
frontend:
  ports:
    - "8080:80"  # 改为 8080 端口
```

然后访问 `http://localhost:8080`

### 2. 数据库连接失败

确保数据库健康检查通过：

```bash
docker-compose logs opengauss
```

如果看到 "database system is ready to accept connections"，说明数据库已就绪。

### 3. 前端无法访问后端 API

检查 Nginx 配置和后端服务状态：

```bash
# 查看后端日志
docker-compose logs backend

# 测试后端 API
curl http://localhost:5000/api/auth/me
```

### 4. 重置所有数据

```bash
# 停止服务并删除数据卷
docker-compose down -v

# 重新启动
docker-compose up --build
```

### 5. 修改 JWT 密钥

在 `docker-compose.yml` 中修改 `JWT_SECRET` 环境变量：

```yaml
backend:
  environment:
    JWT_SECRET: your-new-secret-key-here
```

## 性能优化

### 前端优化

- 使用 Nginx gzip 压缩
- 静态资源缓存（1年）
- 代码分割和懒加载
- 图片优化

### 后端优化

- 数据库连接池（最大 20 个连接）
- JWT token 缓存
- API 响应压缩
- 查询优化和索引

## 安全建议

1. **生产环境必须修改**：
   - 数据库密码（`GS_PASSWORD`）
   - JWT 密钥（`JWT_SECRET`）

2. **启用 HTTPS**：
   - 使用 Let's Encrypt 证书
   - 配置 Nginx SSL

3. **限制数据库访问**：
   - 不要暴露 5432 端口到公网
   - 使用防火墙规则

4. **定期备份数据**：
```bash
docker exec gradient-db gs_dump -U gaussdb postgres > backup.sql
```

## 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目仅用于学习和教学目的。

## 联系方式

如有问题或建议，请提交 Issue。

---

**祝你使用愉快！** 🎨✨
# gradient-generator-tool
