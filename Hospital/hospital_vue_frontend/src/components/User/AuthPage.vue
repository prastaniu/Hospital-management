<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100 bg-light">
    <div class="card shadow-lg p-4" style="width: 100%; max-width: 500px;">
      <h2 class="text-center mb-4 text-primary">{{ isLogin ? 'Login' : 'Register' }}</h2>

      <form @submit.prevent="isLogin ? handleLogin() : handleRegister()">
        <div v-if="!isLogin" class="row">
          <div class="col-md-6 mb-3">
            <label class="form-label">First Name</label>
            <input v-model="form.first_name" type="text" class="form-control" :class="{ 'is-invalid': errors.first_name }" />
            <div v-if="errors.first_name" class="invalid-feedback">{{ errors.first_name }}</div>
          </div>
          <div class="col-md-6 mb-3">
            <label class="form-label">Last Name</label>
            <input v-model="form.last_name" type="text" class="form-control" :class="{ 'is-invalid': errors.last_name }" />
            <div v-if="errors.last_name" class="invalid-feedback">{{ errors.last_name }}</div>
          </div>
        </div>

        <div class="mb-3">
          <label class="form-label">Email</label>
          <input v-model="form.email" type="email" class="form-control" :class="{ 'is-invalid': errors.email }" />
          <div v-if="errors.email" class="invalid-feedback">{{ errors.email }}</div>
        </div>

        <div class="mb-3">
          <label class="form-label">Password</label>
          <input v-model="form.password" type="password" class="form-control" :class="{ 'is-invalid': errors.password }" />
          <div v-if="errors.password" class="invalid-feedback">{{ errors.password }}</div>
        </div>

        <div v-if="!isLogin" class="mb-3">
          <label class="form-label">Confirm Password</label>
          <input v-model="form.confirm_password" type="password" class="form-control" :class="{ 'is-invalid': errors.confirm_password }" />
          <div v-if="errors.confirm_password" class="invalid-feedback">{{ errors.confirm_password }}</div>
        </div>

        <div class="d-grid">
          <button type="submit" class="btn btn-primary">{{ isLogin ? 'Login' : 'Register' }}</button>
        </div>
      </form>

      <div v-if="message" class="alert alert-info mt-3 text-center">{{ message }}</div>

      <div class="text-center mt-3">
        <span>
          {{ isLogin ? "New user?" : "Already registered?" }}
          <a href="#" @click.prevent="toggleMode">{{ isLogin ? "Register here" : "Login here" }}</a>
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AuthPage',
  data() {
    return {
      isLogin: true,
      form: {
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        confirm_password: ''
      },
      errors: {},
      message: ''
    };
  },
  methods: {
    toggleMode() {
      this.isLogin = !this.isLogin;
      this.form = {
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        confirm_password: ''
      };
      this.errors = {};
      this.message = '';
    },
    validateEmail(email) {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return re.test(email);
    },
    async handleLogin() {
      this.errors = {};
      const { email, password } = this.form;

      if (!email) this.errors.email = 'Email is required.';
      else if (!this.validateEmail(email)) this.errors.email = 'Invalid email format.';
      if (!password) this.errors.password = 'Password is required.';

      if (Object.keys(this.errors).length) return;

      try {
        const res = await axios.post('http://127.0.0.1:5000/login', { email, password });
        this.message = res.data.message || 'Login successful!';
        // localStorage.setItem("token", res.data.token)
        // this.$router.push('/dashboard')
      } catch (err) {
        this.message = err.response?.data?.message || 'Login failed.';
      }
    },
    async handleRegister() {
      this.errors = {};
      const f = this.form;

      if (!f.first_name) this.errors.first_name = 'First name is required.';
      if (!f.last_name) this.errors.last_name = 'Last name is required.';
      if (!f.email) this.errors.email = 'Email is required.';
      else if (!this.validateEmail(f.email)) this.errors.email = 'Invalid email format.';
      if (!f.password) this.errors.password = 'Password is required.';
      else if (f.password.length < 6) this.errors.password = 'Password must be at least 6 characters.';
      if (f.confirm_password !== f.password) this.errors.confirm_password = 'Passwords do not match.';

      if (Object.keys(this.errors).length) return;

      try {
        const res = await axios.post('http://127.0.0.1:5000/register', f);
        this.message = res.data.message || 'Registration successful!';
        this.toggleMode(); // switch to login
      } catch (err) {
        this.message = err.response?.data?.message || 'Registration failed.';
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
a {
  cursor: pointer;
}
</style>
