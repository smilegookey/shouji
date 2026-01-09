import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import RegisterView from './views/RegisterView.vue'
import AdminView from './views/AdminView.vue'
import './styles.css'

const routes = [
  { path: '/', redirect: '/register' },
  { path: '/register', component: RegisterView },
  { path: '/admin', component: AdminView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

createApp(App).use(router).mount('#app')
