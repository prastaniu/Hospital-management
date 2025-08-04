<template>
    <div class="container py-4">
        <h2 class="text-center text-primary mb-4">📊 Reports</h2>

        <div class="mb-4 d-flex gap-3 justify-content-center flex-wrap">
            <router-link class="btn btn-outline-dark" to="/reports"
                :class="{ active: $route.path === '/reports' }">Dashboard</router-link>

            <router-link class="btn btn-outline-dark" to="/reports/doctors"
                :class="{ active: $route.path === '/reports/doctors' }">Doctors</router-link>

            <router-link class="btn btn-outline-dark" to="/reports/patients"
                :class="{ active: $route.path === '/reports/patients' }">Patients</router-link>

            <router-link class="btn btn-outline-dark" to="/reports/appointments"
                :class="{ active: $route.path === '/reports/appointments' }">Appointments</router-link>

            <router-link class="btn btn-outline-dark" to="/reports/treatments"
                :class="{ active: $route.path === '/reports/treatments' }">Treatments</router-link>

            <router-link class="btn btn-outline-dark" to="/reports/billings"
                :class="{ active: $route.path === '/reports/billings' }">Billings</router-link>
        </div>

        <router-view />
    </div>
</template>
<style scoped>
.btn {
    min-width: 120px;
}

.router-link-exact-active,
.active {
    background-color: #0d6efd;
    color: white !important;
    border-color: #0d6efd;
}
</style>
<style scoped>
.btn {
    min-width: 120px;
}

.router-link-exact-active,
.active {
    background-color: #0d6efd;
    color: white !important;
    border-color: #0d6efd;
}
</style>
