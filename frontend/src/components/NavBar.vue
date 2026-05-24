<template>
  <nav class="navbar">
    <div class="navbar-container">
      <div class="navbar-left">
        <router-link to="/plaza" class="logo">GradientLab</router-link>
      </div>
      
      <div class="navbar-center">
        <router-link to="/plaza" class="nav-link">广场</router-link>
        <router-link to="/editor" class="nav-link">编辑器</router-link>
        <router-link to="/my-gradients" class="nav-link">我的方案</router-link>
        <router-link to="/favorites" class="nav-link">我的收藏</router-link>
      </div>
      
      <div class="navbar-right">
        <template v-if="!authStore.isAuthenticated">
          <router-link to="/login" class="btn btn-secondary">登录</router-link>
          <router-link to="/register" class="btn btn-primary">注册</router-link>
        </template>
        <template v-else>
          <span class="username">{{ authStore.user?.username }}</span>
          <button @click="handleLogout" class="btn btn-secondary">退出</button>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = () => {
  authStore.logout()
  router.push('/plaza')
}
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 52px;
  background: #141418;
  border-bottom: 1px solid #222230;
  z-index: 1000;
}

.navbar-container {
  max-width: 1400px;
  margin: 0 auto;
  height: 100%;
  display: flex;
  align-items: center;
  gap: 0;
  padding: 0 32px;
}

.navbar-left {
  flex: 0 0 auto;
}

.logo {
  font-size: 17px;
  font-weight: 600;
  margin-right: 40px;
  background: linear-gradient(90deg, #ff6b6b, #c084fc, #4ecdc4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.3px;
  text-decoration: none;
  transition: opacity 0.2s;
}

.logo:hover {
  opacity: 0.8;
}

.navbar-center {
  display: flex;
  gap: 2px;
  flex: 0 0 auto;
}

.nav-link {
  color: #888;
  text-decoration: none;
  font-size: 13px;
  font-weight: 500;
  padding: 6px 14px;
  border-radius: 6px;
  transition: color 0.15s;
}

.nav-link:hover {
  color: #ccc;
}

.nav-link.router-link-active {
  color: #e8e8f0;
  background: #1e1e2a;
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 0 0 auto;
  margin-left: auto;
}

.username {
  color: #aaa;
  font-size: 13px;
  font-weight: 500;
  padding: 0 12px;
}

.btn {
  padding: 5px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  text-decoration: none;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-block;
}

.btn-primary {
  background: linear-gradient(135deg, #ff6b6b, #c084fc);
  color: #ffffff;
}

.btn-primary:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.btn-secondary {
  background: transparent;
  color: #888;
  border: 1px solid #2a2a3a;
}

.btn-secondary:hover {
  color: #ccc;
  border-color: #444;
}
</style>
