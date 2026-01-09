<template>
  <div class="card">
    <h2>用户注册</h2>
    <form @submit.prevent="handleRegister">
      <label>
        邮箱
        <input v-model="form.email" type="email" required />
      </label>
      <label>
        密码（至少 8 位）
        <input v-model="form.password" type="password" minlength="8" required />
      </label>
      <button type="submit">注册</button>
    </form>
    <p v-if="message" :class="messageClass">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'

const apiBase = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api'
const form = ref({
  email: '',
  password: ''
})
const message = ref('')
const success = ref(false)

const messageClass = computed(() => (success.value ? '' : 'notice'))

const handleRegister = async () => {
  message.value = ''
  try {
    await axios.post(`${apiBase}/register`, form.value)
    success.value = true
    message.value = '注册成功，请联系管理员开通权限。'
    form.value = { email: '', password: '' }
  } catch (error) {
    success.value = false
    message.value = error.response?.data?.detail || '注册失败，请稍后再试。'
  }
}
</script>
