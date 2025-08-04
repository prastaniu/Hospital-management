<template>
  <div class="container my-5">
    <div class="card shadow-lg p-4">
      <h2 class="text-center text-primary mb-4">Treatments List</h2>

      <div class="d-flex justify-content-end mb-3">
        <router-link to="/new-treatment" class="btn btn-success">+ Add New Treatment</router-link>
      </div>

      <table class="table table-bordered table-hover text-center">
        <thead class="table-light">
          <tr>
            <th>Treatment ID</th>
            <th>Appointment ID</th>
            <th>Type</th>
            <th>Description</th>
            <th>Cost</th>
            <th>Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="treat in treatments" :key="treat.treatment_id">
            <td>{{ treat.treatment_id }}</td>
            <td>{{ treat.appointment_id }}</td>
            <td>{{ treat.treatment_type }}</td>
            <td>{{ treat.description }}</td>
            <td>${{ treat.cost }}</td>
            <td>{{ treat.treatment_date }}</td>
            <td>
              <button class="btn btn-sm btn-primary me-2" @click="viewTreatment(treat)">View</button>
              <button class="btn btn-sm btn-danger" @click="deleteTreatment(treat.treatment_id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- View Modal -->
      <div v-if="selectedTreatment" class="modal d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.4);">
        <div class="modal-dialog">
          <div class="modal-content p-3">
            <h5 class="modal-title">View Treatment Details</h5>
            <div v-for="(value, key) in selectedTreatment" :key="key" class="mb-2">
              <label class="form-label text-capitalize">{{ key.replace('_', ' ') }}</label>
              <input
                :value="value"
                class="form-control"
                readonly
              />
            </div>
            <div class="mt-3 text-end">
              <button class="btn btn-secondary" @click="closeView">Close</button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="message" class="alert alert-info mt-4 text-center">{{ message }}</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Treatments',
  data() {
    return {
      message: '',
      selectedTreatment: null,
      errors: {},
      treatments: []
    }
  },
  mounted() {
    this.fetchTreatments()
  },
  methods: {
    async fetchTreatments() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/treatments')
        this.treatments = res.data
      } catch (err) {
        console.error('Error fetching treatments:', err)
        this.message = 'Failed to load treatments'
      }
    },
    viewTreatment(treatment) {
      this.selectedTreatment = { ...treatment }
      this.message = ''
      this.errors = {}
    },
    closeView() {
      this.selectedTreatment = null
      this.errors = {}
      this.message = ''
    },
    async deleteTreatment(id) {
      if (!confirm('Are you sure you want to delete this treatment?')) return

      try {
        await axios.delete(`http://127.0.0.1:5000/treatments/${id}`)
        this.message = 'Treatment deleted successfully.'
        this.fetchTreatments()
      } catch (err) {
        console.error('Error deleting treatment:', err)
        this.message = 'Failed to delete treatment.'
      }
    }
  }
}
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
.modal-dialog {
  margin-top: 10%;
}
</style>
