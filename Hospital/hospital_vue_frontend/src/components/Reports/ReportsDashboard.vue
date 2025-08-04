<template>
  <div class="reports-dashboard container my-5">
    <h1 class="text-center mb-4 text-primary">Reports Dashboard</h1>
    <p class="text-center mb-5">
      Welcome! Select a report category below to explore detailed analytics and insights.
    </p>

    <div class="row g-4">
      <div class="col-sm-6 col-md-4 col-lg-3" v-for="report in reports" :key="report.name">
        <router-link :to="report.route" class="card report-card h-100 text-decoration-none text-dark">
          <div class="card-body d-flex flex-column justify-content-center align-items-center">
            <div class="icon mb-3">
              <i :class="report.icon" style="font-size: 3rem;"></i>
            </div>
            <h5 class="card-title">{{ report.label }}</h5>
            <p class="card-text text-muted">{{ report.description }}</p>
          </div>
        </router-link>
      </div>
    </div>

    <!-- Optional: Summary Section -->
    <div class="summary mt-5 p-4 bg-light rounded shadow-sm">
      <h3>Quick Summary</h3>
      <p class="mb-1">Total Doctors: <strong>{{ totalDoctors }}</strong></p>
      <p class="mb-1">Total Patients: <strong>{{ totalPatients }}</strong></p>
      <p class="mb-1">Upcoming Appointments (next 7 days): <strong>{{ upcomingAppointments }}</strong></p>
      <p class="mb-1">Total Billings: <strong>${{ totalBillings }}</strong></p>
    </div>
  </div>
</template>

<script>
export default {
  name: "ReportsDashboard",
  data() {
    return {
      reports: [
        {
          name: "doctorReports",
          label: "Doctors Reports",
          route: "/reports/doctors",
          description: "Doctors by specialization, branch, and experience",
          icon: "fas fa-user-md",
        },
        {
          name: "patientReports",
          label: "Patients Reports",
          route: "/reports/patients",
          description: "Patient demographics and insurance statistics",
          icon: "fas fa-procedures",
        },
        {
          name: "appointmentReports",
          label: "Appointments Reports",
          route: "/reports/appointments",
          description: "Appointment statuses and schedules",
          icon: "fas fa-calendar-check",
        },
        {
          name: "treatmentReports",
          label: "Treatments Reports",
          route: "/reports/treatments",
          description: "Treatment types and cost summaries",
          icon: "fas fa-pills",
        },
        {
          name: "billingReports",
          label: "Billings Reports",
          route: "/reports/billings",
          description: "Billing status and revenue summaries",
          icon: "fas fa-file-invoice-dollar",
        },
      ],
      // These could be computed or fetched from API/store, here static mock
      totalDoctors: 25,
      totalPatients: 120,
      upcomingAppointments: 10,
      totalBillings: 45230,
    };
  },
};
</script>

<style scoped>
.reports-dashboard {
  max-width: 1100px;
  margin-left: auto;
  margin-right: auto;
}

.report-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
  border-radius: 0.5rem;
  box-shadow: 0 2px 6px rgb(0 0 0 / 0.1);
}

.report-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 10px 20px rgb(0 0 0 / 0.15);
}

.icon {
  color: #007bff;
}

.summary h3 {
  border-bottom: 2px solid #007bff;
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;
}
</style>
