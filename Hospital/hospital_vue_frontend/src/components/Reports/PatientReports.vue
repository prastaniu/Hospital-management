<template>
  <div class="container my-5">
    <div class="card shadow-lg p-4">
      <h2 class="text-center text-primary mb-4">Patient Reports</h2>

      <div class="row">
        <div class="col-md-6 mb-4">
          <h5 class="text-center">Patients by Insurance Provider</h5>
          <BarChart :chart-data="insuranceChartData" />
        </div>

        <div class="col-md-6 mb-4">
  <h5 class="text-center">Patient Gender Distribution</h5>
  <div class="pie-chart-container">
    <PieChart :chart-data="genderChartData" />
  </div>
</div>


        <div class="col-md-12">
          <h5 class="text-center">New Patients Registered Per Month</h5>
          <LineChart :chart-data="monthlyChartData" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import BarChart from '../Charts/BarChart.vue'
import PieChart from '../Charts/PieChart.vue'
import LineChart from '../Charts/LineChart.vue'

export default {
  name: 'PatientReports',
  components: { BarChart, PieChart, LineChart },
  data() {
    return {
      patients: [],
      loading: true,
    }
  },
  computed: {
    insuranceChartData() {
      const counts = {}
      this.patients.forEach(p => {
        counts[p.insurance_provider] = (counts[p.insurance_provider] || 0) + 1
      })
      return {
        labels: Object.keys(counts),
        datasets: [{
          label: 'Patients',
          backgroundColor: '#42A5F5',
          data: Object.values(counts)
        }]
      }
    },
    genderChartData() {
      const genderCounts = {}
      this.patients.forEach(p => {
        genderCounts[p.gender] = (genderCounts[p.gender] || 0) + 1
      })
      return {
        labels: Object.keys(genderCounts),
        datasets: [{
          label: 'Gender Distribution',
          backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
          data: Object.values(genderCounts)
        }]
      }
    },
    monthlyChartData() {
      const monthCounts = {}
      this.patients.forEach(p => {
        const month = new Date(p.registration_date).toLocaleString('default', { month: 'short', year: 'numeric' })
        monthCounts[month] = (monthCounts[month] || 0) + 1
      })

      const sortedMonths = Object.keys(monthCounts).sort((a, b) =>
        new Date(`1 ${a}`) - new Date(`1 ${b}`)
      )

      return {
        labels: sortedMonths,
        datasets: [{
          label: 'New Patients',
          borderColor: '#4CAF50',
          data: sortedMonths.map(m => monthCounts[m]),
          fill: false
        }]
      }
    }
  },
  methods: {
    async fetchPatients() {
      try {
        const response = await axios.get('http://localhost:5000/patients') // Replace with your actual backend URL
        this.patients = response.data
      } catch (error) {
        console.error('Error fetching patients:', error)
      } finally {
        this.loading = false
      }
    }
  },
  mounted() {
    this.fetchPatients()
  }
}
</script>

<style scoped>
h5 {
  font-weight: 600;
}
.pie-chart-container {
  max-width: 300px; /* adjust width as needed */
  max-height: 300px; /* adjust height as needed */
  margin: 0 auto;    /* center horizontally */
}

</style>
