<template>
  <div class="d-flex justify-content-center my-5">
    <div class="card shadow-lg p-4" style="max-width: 800px; width: 100%;">
      <!-- Back Button -->
      <div class="mb-3 text-end">
        <router-link to="/treatments" class="btn btn-outline-secondary">
          ← Back
        </router-link>
      </div>
      <h2 class="text-center text-primary mb-4">Add Treatment</h2>

      <form @submit.prevent="submitTreatment">
        <div class="mb-3">
          <label class="form-label">Treatment ID</label>
          <input
            v-model="form.treatment_id"
            class="form-control"
            :class="{ 'is-invalid': errors.treatment_id }"
          />
          <div v-if="errors.treatment_id" class="invalid-feedback">{{ errors.treatment_id }}</div>
        </div>

        <div class="mb-3">
          <label class="form-label">Appointment ID</label>
          <input
            v-model="form.appointment_id"
            class="form-control"
            :class="{ 'is-invalid': errors.appointment_id }"
          />
          <div v-if="errors.appointment_id" class="invalid-feedback">{{ errors.appointment_id }}</div>
        </div>

        <div class="mb-3">
          <label class="form-label">Treatment Type</label>
          <input
            v-model="form.treatment_type"
            class="form-control"
            :class="{ 'is-invalid': errors.treatment_type }"
          />
          <div v-if="errors.treatment_type" class="invalid-feedback">{{ errors.treatment_type }}</div>
        </div>

        <div class="mb-3">
          <label class="form-label">Description</label>
          <input v-model="form.description" class="form-control" />
        </div>

        <div class="mb-3">
          <label class="form-label">Cost</label>
          <input
            v-model="form.cost"
            class="form-control"
            :class="{ 'is-invalid': errors.cost }"
          />
          <div v-if="errors.cost" class="invalid-feedback">{{ errors.cost }}</div>
        </div>

        <div class="mb-3">
          <label class="form-label">Date</label>
          <input
            v-model="form.treatment_date"
            type="date"
            class="form-control"
            :class="{ 'is-invalid': errors.treatment_date }"
          />
          <div v-if="errors.treatment_date" class="invalid-feedback">{{ errors.treatment_date }}</div>
        </div>

        <div class="text-center">
          <button type="submit" class="btn btn-primary">Submit</button>
        </div>
      </form>

      <div v-if="message" class="alert alert-info mt-3 text-center">{{ message }}</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'NewTreatment',
  data() {
    return {
      form: {
        treatment_id: '',
        appointment_id: '',
        treatment_type: '',
        description: '',
        cost: '',
        treatment_date: ''
      },
      message: '',
      errors: {}
    }
  },
  methods: {
    validateForm() {
      this.errors = {}

      if (!this.form.treatment_id) this.errors.treatment_id = 'Treatment ID is required.'
      if (!this.form.appointment_id) this.errors.appointment_id = 'Appointment ID is required.'
      if (!this.form.treatment_type) this.errors.treatment_type = 'Treatment type is required.'
      if (!this.form.cost) {
        this.errors.cost = 'Cost is required.'
      } else if (isNaN(this.form.cost) || Number(this.form.cost) <= 0) {
        this.errors.cost = 'Cost must be a positive number.'
      }
      if (!this.form.treatment_date) this.errors.treatment_date = 'Treatment date is required.'

      return Object.keys(this.errors).length === 0
    },

    async submitTreatment() {
      if (!this.validateForm()) {
        this.message = 'Please fix errors before submitting.'
        return
      }
      this.message = ''
      try {
        const res = await axios.post('http://localhost:5000/treatments', this.form)
        this.message = res.data.message || 'Treatment added!'
        this.clearForm()
      } catch (err) {
        this.message = 'Error: ' + (err.response?.data?.message || err.message)
      }
    },

    clearForm() {
      this.form = {
        treatment_id: '',
        appointment_id: '',
        treatment_type: '',
        description: '',
        cost: '',
        treatment_date: ''
      }
      this.errors = {}
    }
  }
}
</script>

<style scoped>
.is-invalid {
  border-color: #dc3545;
}

.invalid-feedback {
  color: #dc3545;
  font-size: 0.875em;
  margin-top: 0.25rem;
}
</style>
