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
  height: 70px;
  background: #1a1a24;
  border-bottom: 1px solid #2a2a3a;
  z-index: 1000;
}

.navbar-container {
  max-width: 1400px;
  margin: 0 auto;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
}

.navbar-left {
  flex: 0 0 auto;
}

.logo {
  font-size: 24px;
  font-weight: 700;
  color: #7c6aff;
  text-decoration: none;
  transition: opacity 0.2s;
}

.logo:hover {
  opacity: 0.8;
}

.navbar-center {
  display: flex;
  gap: 32px;
  flex: 1;
  justify-content: center;
}

.nav-link {
  color: #a0a0b0;
  text-decoration: none;
  font-size: 15px;
  font-weight: 500;
  transition: color 0.2s;
  position: relative;
}

.nav-link:hover {
  color: #ffffff;
}

.nav-link.router-link-active {
  color: #7c6aff;
}

.nav-link.router-link-active::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  right: 0;
  height: 2px;
  background: #7c6aff;
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 0 0 auto;
}

.username {
  color: #ffffff;
  font-size: 14px;
  font-weight: 500;
  padding: 0 12px;
}

.btn {
  padding: 8px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-block;
}

.btn-primary {
  background: #7c6aff;
  color: #ffffff;
}

.btn-primary:hover {
  background: #6a58e6;
  transform: translateY(-1px);
}

.btn-secondary {
  background: transparent;
  color: #a0a0b0;
  border: 1px solid #2a2a3a;
}

.btn-secondary:hover {
  color: #ffffff;
  border-color: #3a3a4a;
}
</style>
