<template>
  <div class="container my-5">
    <div class="card shadow-lg p-4">
      <h2 class="text-center text-primary mb-4">Treatment Reports</h2>

      <div v-if="loading" class="text-center my-5">
        Loading treatments...
      </div>

      <div v-else-if="error" class="alert alert-danger text-center">
        {{ error }}
      </div>

      <div v-else>
        <!-- Summary -->
        <div class="col-md-12 mb-4">
          <h5 class="text-center">Treatment Cost Summary</h5>
          <div class="row text-center">
            <div class="col-md-3">
              <div class="bg-light rounded p-3 shadow-sm">
                <strong>Total Cost</strong>
                <div class="text-success h5">${{ totalCost.toFixed(2) }}</div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="bg-light rounded p-3 shadow-sm">
                <strong>Average Cost</strong>
                <div class="text-primary h5">${{ averageCost.toFixed(2) }}</div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="bg-light rounded p-3 shadow-sm">
                <strong>Highest Cost</strong>
                <div class="text-danger h5">${{ maxCost.toFixed(2) }}</div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="bg-light rounded p-3 shadow-sm">
                <strong>Lowest Cost</strong>
                <div class="text-muted h5">${{ minCost.toFixed(2) }}</div>
              </div>
            </div>
          </div>
        </div>

       <!-- Chart and Table Wrapper -->
<div class="row justify-content-center">
  <!-- Chart -->
  <div class="col-md-6 mb-4">
    <h5 class="text-center">Treatments by Type</h5>
    <BarChart :chart-data="treatmentsByTypeData" />
  </div>

  <!-- Table -->
  <div class="col-md-6 mb-4">
    <h5 class="text-center">Treatments per Appointment</h5>
    <table class="table table-sm table-bordered text-center">
      <thead class="table-light">
        <tr>
          <th>Appointment ID</th>
          <th># of Treatments</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(count, apptId) in treatmentsPerAppointment" :key="apptId">
          <td>{{ apptId }}</td>
          <td>{{ count }}</td>
        </tr>
      </tbody>
    </table>
  </div></div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import BarChart from '../Charts/BarChart.vue'

export default {
  name: 'TreatmentReports',
  components: { BarChart },
  data() {
    return {
      treatments: [],
      loading: true,
      error: null
    }
  },
  computed: {
    totalCost() {
      return this.treatments.reduce((sum, t) => sum + (parseFloat(t.cost) || 0), 0)
    },
    averageCost() {
      return this.treatments.length ? this.totalCost / this.treatments.length : 0
    },
    maxCost() {
      return this.treatments.length ? Math.max(...this.treatments.map(t => parseFloat(t.cost) || 0)) : 0
    },
    minCost() {
      return this.treatments.length ? Math.min(...this.treatments.map(t => parseFloat(t.cost) || 0)) : 0
    },
    treatmentsByTypeData() {
      const counts = {}
      this.treatments.forEach(t => {
        counts[t.treatment_type] = (counts[t.treatment_type] || 0) + 1
      })
      return {
        labels: Object.keys(counts),
        datasets: [
          {
            label: 'Number of Treatments',
            backgroundColor: '#42A5F5',
            data: Object.values(counts)
          }
        ]
      }
    },
    treatmentsPerAppointment() {
      const map = {}
      this.treatments.forEach(t => {
        map[t.appointment_id] = (map[t.appointment_id] || 0) + 1
      })
      return map
    }
  },
  methods: {
    async fetchTreatments() {
      try {
        const res = await axios.get('http://localhost:5000/treatments') // Adjust if deployed
        this.treatments = res.data
      } catch (err) {
        this.error = 'Failed to load treatment data. Please try again.'
        console.error(err)
      } finally {
        this.loading = false
      }
    }
  },
  mounted() {
    this.fetchTreatments()
  }
}
</script>

<style scoped>
h5 {
  font-weight: 600;
}
</style>
