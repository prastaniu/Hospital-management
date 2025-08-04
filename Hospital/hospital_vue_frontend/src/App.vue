<template>
  <div>
    <!-- Top bar -->
    <div class="bg-primary text-white d-flex justify-content-between align-items-center px-3 py-2 small">
      <div class="d-flex gap-3">
        <i class="fab fa-facebook-f me-2"></i>
        <i class="fab fa-twitter me-2"></i>
        <i class="fab fa-pinterest"></i>
      </div>
      <div class="d-flex gap-4">
        <span>+1-123-556-5523</span>
        <span>support@example.com</span>
      </div>
    </div>

    <!-- Header and Navigation -->
    <header class="d-flex justify-content-between align-items-center px-4 py-3 shadow">
      <h1 class="h4 text-primary fw-bold">Hospital <span class="text-dark">Management</span></h1>
      <nav>
        <ul class="nav">
          <li class="nav-item">
            <router-link class="nav-link" to="/">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/doctors">Doctors</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/appointments">Appointments</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/patients">Patients</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/treatments">Treatments</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/billings">Billings</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/reports">Reports</router-link>
          </li>
        </ul>
      </nav>
    </header>

    <!-- Routed component goes here -->
    <main>
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
/* Optional global styles */
body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
</style>
