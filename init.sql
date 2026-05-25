-- 数据库初始化脚本
-- 用于 OpenGauss / PostgreSQL

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id          SERIAL PRIMARY KEY,
    username    VARCHAR(50)  UNIQUE NOT NULL,
    password    VARCHAR(255) NOT NULL,
    created_at  TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- 创建渐变方案表
CREATE TABLE IF NOT EXISTS gradients (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER      NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name        VARCHAR(100) NOT NULL DEFAULT '未命名方案',
    type        VARCHAR(10)  NOT NULL CHECK (type IN ('linear', 'radial')),
    angle       INTEGER      NOT NULL DEFAULT 90,
    stops       JSONB        NOT NULL,
    css_value   TEXT         NOT NULL,
    is_public   BOOLEAN      NOT NULL DEFAULT false,
    created_at  TIMESTAMP    NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- 创建收藏表（多对多关系）
CREATE TABLE IF NOT EXISTS favorites (
    user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    gradient_id INTEGER NOT NULL REFERENCES gradients(id) ON DELETE CASCADE,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (user_id, gradient_id)
);

-- 创建索引以提升查询性能
CREATE INDEX IF NOT EXISTS idx_gradients_user_id ON gradients(user_id);
CREATE INDEX IF NOT EXISTS idx_gradients_is_public ON gradients(is_public);
CREATE INDEX IF NOT EXISTS idx_gradients_created_at ON gradients(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_favorites_user_id ON favorites(user_id);
CREATE INDEX IF NOT EXISTS idx_favorites_gradient_id ON favorites(gradient_id);

