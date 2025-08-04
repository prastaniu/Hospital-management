<template>
  <div class="container mt-5" style="max-width: 400px;">
    <h3 class="text-center mb-4">Login</h3>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <form @submit.prevent="login">
      <div class="mb-3">
        <label class="form-label">Username</label>
        <input v-model="username" class="form-control" required />
      </div>
      <div class="mb-3">
        <label class="form-label">Password</label>
        <input type="password" v-model="password" class="form-control" required />
      </div>
      <button class="btn btn-primary w-100" type="submit">Login</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      error: ''
    }
  },
  methods: {
    login() {
      // Hardcoded login
      if (this.username === 'admin' && this.password === 'admin') {
        localStorage.setItem('token', 'fake-jwt-token')
        localStorage.setItem('username', this.username)
        localStorage.setItem('role', 'admin')  // You can check this role later
        this.$router.push('/')
      } else {
        this.error = 'Invalid username or password'
      }
    }
  }
}
</script>
