<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-card">
        <h1 class="title">注册</h1>
        <p class="subtitle">加入 GradientLab 开始创作</p>
        
        <form @submit.prevent="handleRegister" class="register-form">
          <div class="form-group">
            <label for="username">用户名</label>
            <input
              id="username"
              v-model="username"
              type="text"
              placeholder="3-20位字母数字"
              :disabled="loading"
              required
            />
          </div>
          
          <div class="form-group">
            <label for="password">密码</label>
            <input
              id="password"
              v-model="password"
              type="password"
              placeholder="至少6位"
              :disabled="loading"
              required
            />
          </div>
          
          <div class="form-group">
            <label for="confirmPassword">确认密码</label>
            <input
              id="confirmPassword"
              v-model="confirmPassword"
              type="password"
              placeholder="再次输入密码"
              :disabled="loading"
              required
            />
          </div>
          
          <div v-if="error" class="error-message">{{ error }}</div>
          
          <button type="submit" class="btn btn-primary btn-block" :disabled="loading">
            {{ loading ? '注册中...' : '注册' }}
          </button>
        </form>
        
        <div class="footer-link">
          已有账号？<router-link to="/login">去登录</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref('')

const validateForm = () => {
  if (!username.value || !password.value || !confirmPassword.value) {
    error.value = '请填写完整信息'
    return false
  }
  
  if (!/^[a-zA-Z0-9]{3,20}$/.test(username.value)) {
    error.value = '用户名必须是3-20位字母数字'
    return false
  }
  
  if (password.value.length < 6) {
    error.value = '密码至少6位'
    return false
  }
  
  if (password.value !== confirmPassword.value) {
    error.value = '两次密码输入不一致'
    return false
  }
  
  return true
}

const handleRegister = async () => {
  if (!validateForm()) return
  
  loading.value = true
  error.value = ''
  
  try {
    await authStore.register(username.value, password.value)
    router.push('/editor')
  } catch (err) {
    error.value = err.response?.data?.error || '注册失败，请稍后重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #0f0f13;
  padding: 24px;
}

.register-container {
  width: 100%;
  max-width: 420px;
}

.register-card {
  background: #1a1a24;
  border: 1px solid #2a2a3a;
  border-radius: 16px;
  padding: 48px 40px;
}

.title {
  font-size: 32px;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 8px 0;
  text-align: center;
}

.subtitle {
  font-size: 15px;
  color: #a0a0b0;
  margin: 0 0 32px 0;
  text-align: center;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 14px;
  font-weight: 500;
  color: #ffffff;
}

.form-group input {
  width: 100%;
  padding: 12px 16px;
  background: #0f0f13;
  border: 1px solid #2a2a3a;
  border-radius: 8px;
  color: #ffffff;
  font-size: 15px;
  transition: all 0.2s;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: #7c6aff;
  box-shadow: 0 0 0 3px rgba(124, 106, 255, 0.1);
}

.form-group input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.form-group input::placeholder {
  color: #5a5a6a;
}

.error-message {
  padding: 12px 16px;
  background: rgba(255, 107, 107, 0.1);
  border: 1px solid rgba(255, 107, 107, 0.3);
  border-radius: 8px;
  color: #ff6b6b;
  font-size: 14px;
}

.btn {
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: #7c6aff;
  color: #ffffff;
}

.btn-primary:hover:not(:disabled) {
  background: #6a58e6;
  transform: translateY(-1px);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-block {
  width: 100%;
}

.footer-link {
  margin-top: 24px;
  text-align: center;
  font-size: 14px;
  color: #a0a0b0;
}

.footer-link a {
  color: #7c6aff;
  text-decoration: none;
  font-weight: 500;
}

.footer-link a:hover {
  text-decoration: underline;
}
</style>
