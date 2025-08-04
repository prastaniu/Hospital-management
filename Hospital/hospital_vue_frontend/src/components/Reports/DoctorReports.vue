<template>
  <div class="container my-5">
    <!-- Export Button -->
    <div class="text-end mb-3">
      <button class="btn btn-outline-danger" @click="exportPDF">📄 Export to PDF</button>
    </div>

    <!-- Report Content to Export -->
    <div class="card shadow-lg p-4 pdf-wrapper" ref="reportContent">
      <h2 class="text-primary text-center mb-4">Doctor's Reports</h2>

      <!-- Doctors by Specialization -->
      <div class="charts-row mb-4">
        <div class="chart-container me-3">
          <h4 class="mb-2">Doctors by Specialization</h4>
          <BarChart :data="specializationChartData" />
        </div>

        <!-- Doctors by Hospital Branch -->
        <div class="chart-container">
          <h4 class="mb-2">Doctors by Hospital Branch</h4>
          <BarChart :data="branchChartData" />
        </div>
      </div><br></br><br></br>

      <!-- Average Years of Experience -->
      <div class="mb-4 average-experience-container text-center">
        <div class="alert alert-info fs-5">
          Doctor's Average Experience: <strong>{{ averageExperience }} years</strong>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BarChart from '../Charts/BarChart.vue'
import html2pdf from 'html2pdf.js'
import axios from 'axios'

export default {
  name: 'DoctorReports',
  components: { BarChart },
  data() {
    return {
      doctors: [],      // initialize empty array for doctors
      loading: true,    // optional, if you want to show loading indicator
    }
  },
  computed: {
    specializationChartData() {
      const counts = {}
      this.doctors.forEach(doc => {
        counts[doc.specialization] = (counts[doc.specialization] || 0) + 1
      })
      return {
        labels: Object.keys(counts),
        datasets: [{
          label: 'Doctors',
          data: Object.values(counts),
          backgroundColor: '#0d6efd'
        }]
      }
    },
    branchChartData() {
      const counts = {}
      this.doctors.forEach(doc => {
        counts[doc.hospital_branch] = (counts[doc.hospital_branch] || 0) + 1
      })
      return {
        labels: Object.keys(counts),
        datasets: [{
          label: 'Doctors',
          data: Object.values(counts),
          backgroundColor: '#198754'
        }]
      }
    },
    averageExperience() {
      if (this.doctors.length === 0) return 0
      const total = this.doctors.reduce((sum, doc) => sum + doc.years_experience, 0)
      return (total / this.doctors.length).toFixed(1)
    }
  },
  methods: {
    async fetchDoctors() {
      try {
        const res = await axios.get('http://localhost:5000/doctors')  // Your backend API endpoint
        this.doctors = res.data
      } catch (error) {
        console.error('Error fetching doctors:', error)
      } finally {
        this.loading = false
      }
    },
    exportPDF() {
      const element = this.$refs.reportContent
      const options = {
        margin: 10,
        filename: 'DoctorReport.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
      }
      html2pdf().set(options).from(element).save()
    }
  },
  mounted() {
    this.fetchDoctors()
  }
}
</script>

<style scoped>
.alert {
  background-color: #e8f0fe;
  border-left: 5px solid #0d6efd;
  display: inline-block;
  /* Make alert inline block */
  max-width: 100%;
  /* Full container width */
  padding: 0.5rem 1rem;
  /* Comfortable padding */
  word-break: break-word;
  /* Allow breaking long words */
  white-space: normal;
  /* Allow wrapping */
  font-size: 1.1rem;
  /* Slightly bigger for readability */
}


/* Force canvas to fit in PDF */
canvas {
  max-width: 100% !important;
  height: auto !important;
}

/* Optional: Reduce spacing and text size for PDF clarity */
.pdf-wrapper {
  font-size: 12px;
  line-height: 1.4;
}

.charts-row {
  display: flex;
  gap: 1rem;
  /* spacing between charts */
  justify-content: center;
  flex-wrap: wrap;
  /* wrap on small screens */
}

.chart-container {
  flex: 1 1 45%;
  /* grow, shrink, base 45% width */
  height: 300px;
  max-width: 600px;
  margin: 0 auto;
  min-width: 280px;
  /* optional minimum for small screens */
}

.average-experience-container {
  max-width: 400px;
  /* Adjust width as needed */
  margin: 0 auto;
  /* Center horizontally */
}
</style>
