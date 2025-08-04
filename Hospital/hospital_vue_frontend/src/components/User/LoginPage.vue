<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100 bg-light">
    <div class="card shadow p-4" style="width: 100%; max-width: 400px;">
      <h2 class="text-center text-primary mb-4">Login</h2>

      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input
            type="email"
            v-model="form.email"
            class="form-control"
            :class="{ 'is-invalid': errors.email }"
            id="email"
            placeholder="Enter your email"
          />
          <div v-if="errors.email" class="invalid-feedback">{{ errors.email }}</div>
        </div>

        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input
            type="password"
            v-model="form.password"
            class="form-control"
            :class="{ 'is-invalid': errors.password }"
            id="password"
            placeholder="Enter your password"
          />
          <div v-if="errors.password" class="invalid-feedback">{{ errors.password }}</div>
        </div>

        <div class="d-grid">
          <button type="submit" class="btn btn-primary">Login</button>
        </div>
      </form>

      <div v-if="message" class="alert alert-info mt-3 text-center">{{ message }}</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LoginPage',
  data() {
    return {
      form: {
        email: '',
        password: ''
      },
      errors: {},
      message: ''
    };
  },
  methods: {
    async handleLogin() {
      this.errors = {};

      if (!this.form.email) {
        this.errors.email = 'Email is required.';
      }
      if (!this.form.password) {
        this.errors.password = 'Password is required.';
      }

      if (Object.keys(this.errors).length) return;

      try {
        const res = await axios.post('http://127.0.0.1:5000/login', this.form);
        this.message = res.data.message || 'Login successful!';
        // Store token or redirect user
        // localStorage.setItem('token', res.data.token)
        // this.$router.push('/dashboard')
      } catch (err) {
        this.message = err.response?.data?.message || 'Login failed. Please try again.';
      }
    }
  }
};
</script>

<style scoped>
.card {
  border-radius: 1rem;
}
.is-invalid {
  border-color: #dc3545;
}
.invalid-feedback {
  font-size: 0.875em;
}
</style>
