<template>
  <div class="container">
    <header>
      <h1>手机接码平台</h1>
      <nav>
        <router-link to="/register">用户注册</router-link>
        <span> | </span>
        <router-link to="/admin">后台管理</router-link>
      </nav>
    </header>
    <main style="margin-top: 24px;">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
nav a {
  color: #2563eb;
  text-decoration: none;
  margin-right: 8px;
}
</style>
