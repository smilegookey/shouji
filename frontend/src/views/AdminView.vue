<template>
  <div class="card">
    <h2>管理员后台</h2>
    <div v-if="!token">
      <form @submit.prevent="handleLogin">
        <label>
          管理员邮箱
          <input v-model="loginForm.email" type="email" required />
        </label>
        <label>
          密码
          <input v-model="loginForm.password" type="password" required />
        </label>
        <button type="submit">登录</button>
      </form>
    </div>
    <div v-else>
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span>已登录：{{ adminEmail }}</span>
        <button class="secondary" @click="handleLogout">退出</button>
      </div>
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>邮箱</th>
            <th>状态</th>
            <th>管理员</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.email }}</td>
            <td>
              <span class="badge" :class="user.is_active ? 'active' : 'inactive'">
                {{ user.is_active ? '启用' : '停用' }}
              </span>
            </td>
            <td>{{ user.is_admin ? '是' : '否' }}</td>
            <td>
              <button class="secondary" @click="toggleUser(user)">
                {{ user.is_active ? '停用' : '启用' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <p v-if="message" class="notice">{{ message }}</p>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'

const apiBase = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api'
const token = ref(localStorage.getItem('admin_token') || '')
const adminEmail = ref('')
const users = ref([])
const message = ref('')
const loginForm = ref({
  email: '',
  password: ''
})

const api = axios.create({
  baseURL: apiBase
})

api.interceptors.request.use((config) => {
  if (token.value) {
    config.headers.Authorization = `Bearer ${token.value}`
  }
  return config
})

const loadUsers = async () => {
  try {
    const response = await api.get('/admin/users')
    users.value = response.data
  } catch (error) {
    message.value = error.response?.data?.detail || '获取用户失败'
  }
}

const loadMe = async () => {
  try {
    const response = await api.get('/me')
    adminEmail.value = response.data.email
  } catch (error) {
    message.value = error.response?.data?.detail || '获取管理员信息失败'
  }
}

const handleLogin = async () => {
  message.value = ''
  try {
    const response = await api.post('/login', loginForm.value)
    token.value = response.data.access_token
    localStorage.setItem('admin_token', token.value)
    await loadMe()
    await loadUsers()
  } catch (error) {
    message.value = error.response?.data?.detail || '登录失败'
  }
}

const handleLogout = () => {
  token.value = ''
  adminEmail.value = ''
  users.value = []
  localStorage.removeItem('admin_token')
}

const toggleUser = async (user) => {
  message.value = ''
  try {
    const response = await api.patch(`/admin/users/${user.id}`, {
      is_active: !user.is_active
    })
    const updated = response.data
    users.value = users.value.map((item) => (item.id === updated.id ? updated : item))
  } catch (error) {
    message.value = error.response?.data?.detail || '更新失败'
  }
}

onMounted(async () => {
  if (token.value) {
    await loadMe()
    await loadUsers()
  }
})
</script>
