<template>
  <div class="container my-5">
    <div class="text-end mb-3">
      <button class="btn btn-outline-danger" @click="exportPDF">📄 Export to PDF</button>
    </div>

    <div class="card shadow-lg p-4" ref="reportContent">
      <h2 class="text-center text-primary mb-4">Appointment Reports</h2>

      <div class="row">
        <!-- Chart 1: Appointments by Status -->
        <div class="col-md-6 mb-4 chart-container">
          <h5 class="text-center">Appointments by Status</h5>
          <PieChart :chart-data="statusChartData" />
        </div>

        <!-- Chart 2: Appointments per Doctor -->
        <div class="col-md-6 mb-4 chart-container">
          <h5 class="text-center">Appointments per Doctor</h5>
          <BarChart :chart-data="appointmentsPerDoctorData" />
        </div>

        <!-- Table: Upcoming Appointments -->
        <div class="col-md-12">
          <h5 class="text-center mt-4">Upcoming Appointments (Next 7 Days)</h5>
          <table class="table table-striped table-bordered text-center mt-3">
            <thead class="table-light">
              <tr>
                <th>Appointment ID</th>
                <th>Patient ID</th>
                <th>Doctor</th>
                <th>Date</th>
                <th>Time</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="appt in upcomingAppointments" :key="appt.appointment_id">
                <td>{{ appt.appointment_id }}</td>
                <td>{{ appt.patient_id }}</td>
                <td>{{ getDoctorName(appt.doctor_id) }}</td>
                <td>{{ appt.appointment_date }}</td>
                <td>{{ appt.appointment_time }}</td>
                <td>{{ appt.status }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import html2pdf from 'html2pdf.js'
import BarChart from '../Charts/BarChart.vue'
import PieChart from '../Charts/PieChart.vue'

export default {
  name: 'AppointmentReports',
  components: { BarChart, PieChart },
  data() {
    return {
      doctors: [],
      appointments: [],
      loading: true,
    }
  },
  computed: {
    statusChartData() {
      const statusCounts = {}
      this.appointments.forEach(a => {
        statusCounts[a.status] = (statusCounts[a.status] || 0) + 1
      })
      return {
        labels: Object.keys(statusCounts),
        datasets: [
          {
            label: 'Appointments by Status',
            backgroundColor: ['#42A5F5', '#66BB6A', '#EF5350'],
            data: Object.values(statusCounts)
          }
        ]
      }
    },
    appointmentsPerDoctorData() {
      const doctorCounts = {}
      this.appointments.forEach(a => {
        const name = this.getDoctorName(a.doctor_id)
        doctorCounts[name] = (doctorCounts[name] || 0) + 1
      })
      return {
        labels: Object.keys(doctorCounts),
        datasets: [
          {
            label: 'Appointments per Doctor',
            backgroundColor: '#FFA726',
            data: Object.values(doctorCounts)
          }
        ]
      }
    },
    upcomingAppointments() {
      const today = new Date()
      const weekFromNow = new Date()
      weekFromNow.setDate(today.getDate() + 7)

      return this.appointments.filter(a => {
        const date = new Date(a.appointment_date)
        return date >= today && date <= weekFromNow
      })
    }
  },
  methods: {
    getDoctorName(doctorId) {
      const doc = this.doctors.find(d => d.doctor_id === doctorId)
      return doc ? doc.name : 'Unknown'
    },
    async fetchDoctors() {
      try {
        const res = await axios.get('http://localhost:5000/doctors')  
        this.doctors = res.data
      } catch (error) {
        console.error('Error fetching doctors:', error)
      }
    },
    async fetchAppointments() {
      try {
        const res = await axios.get('http://localhost:5000/appointments') 
        this.appointments = res.data
      } catch (error) {
        console.error('Error fetching appointments:', error)
      }
    },
    exportPDF() {
      const element = this.$refs.reportContent
      const options = {
        margin: 10,
        filename: 'AppointmentReport.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2, useCORS: true },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
      }
      setTimeout(() => {
        html2pdf().set(options).from(element).save()
      }, 500) // delay to ensure charts render
    }
  },
  async mounted() {
    await Promise.all([this.fetchDoctors(), this.fetchAppointments()])
    this.loading = false
  }
}
</script>

<style scoped>
h5 {
  font-weight: 600;
}

/* Ensure charts and tables fit properly in PDF */
canvas {
  max-width: 100% !important;
  height: auto !important;
  display: block;
  margin: 0 auto;
}

/* Add spacing between sections for PDF clarity */
.row > div {
  page-break-inside: avoid;
  margin-bottom: 20px;
}

/* Handle large content gracefully */
table {
  font-size: 12px;
}

/* Prevent overlapping during PDF export */
.card {
  overflow: visible;
}

/* Fix equal height for both chart containers */
.chart-container {
  height: 320px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

/* Ensure canvas fills the container height */
.chart-container canvas {
  max-height: 300px !important;
  width: 100% !important;
  height: 300px !important;
}

@media print {
  .card {
    box-shadow: none !important;
  }
}
</style>
