<template>
  <div class="container my-5">
    <h3 class="text-center">Register</h3>
    <form @submit.prevent="register">
      <input v-model="username" placeholder="Username" required class="form-control mb-3" />
      <input v-model="email" placeholder="Email" required class="form-control mb-3" />
      <input v-model="password" type="password" placeholder="Password" required class="form-control mb-3" />
      <button class="btn btn-success w-100">Register</button>
      <p v-if="message" class="text-success mt-2 text-center">{{ message }}</p>
      <p v-if="error" class="text-danger mt-2 text-center">{{ error }}</p>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      message: '',
      error: ''
    }
  },
  methods: {
    async register() {
      try {
        const res = await axios.post('http://localhost:5000/register', {
          username: this.username,
          email: this.email,
          password: this.password
        })
        this.message = res.data.message
        this.error = ''
      } catch (err) {
        this.error = err.response?.data?.message || 'Registration failed'
        this.message = ''
      }
    }
  }
}
</script>
