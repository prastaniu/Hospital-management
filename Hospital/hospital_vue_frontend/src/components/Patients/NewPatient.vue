<template>
  <div class="d-flex justify-content-center my-5">
    <div class="card shadow-lg p-4" style="max-width: 900px; width: 100%;">

      <!-- Back Button -->
      <div class="mb-3">
        <router-link to="/patients" class="btn btn-outline-secondary">
          ← Back
        </router-link>
      </div>

      <h2 class="mb-4 text-primary text-center">Add New Patient</h2>

      <form @submit.prevent="submitPatient">
        <div class="row g-3">
          <div class="col-md-6">
            <label class="form-label">Patient ID</label>
            <input
              v-model="form.patient_id"
              class="form-control"
              placeholder="PAT123"
              :class="{ 'is-invalid': errors.patient_id }"
            />
            <div v-if="errors.patient_id" class="invalid-feedback">{{ errors.patient_id }}</div>
          </div>

          <div class="col-md-6">
            <label class="form-label">First Name</label>
            <input
              v-model="form.first_name"
              class="form-control"
              :class="{ 'is-invalid': errors.first_name }"
            />
            <div v-if="errors.first_name" class="invalid-feedback">{{ errors.first_name }}</div>
          </div>

          <div class="col-md-6">
            <label class="form-label">Last Name</label>
            <input
              v-model="form.last_name"
              class="form-control"
              :class="{ 'is-invalid': errors.last_name }"
            />
            <div v-if="errors.last_name" class="invalid-feedback">{{ errors.last_name }}</div>
          </div>

          <div class="col-md-6">
            <label class="form-label">Gender</label>
             
            <select v-model="form.gender" class="form-select" 
              :class="{ 'is-invalid': errors.gender }">
              <option disabled value="">Select</option>
              <option value="M">Male</option>
              <option value="F">Female</option>
              <option value="O">Other</option>
            </select>            
            <div v-if="errors.gender" class="invalid-feedback">{{ errors.gender }}</div>
          </div>

          <div class="col-md-6">
            <label class="form-label">Date of Birth</label>
            <input
              type="date"
              v-model="form.date_of_birth"
              class="form-control"
              :class="{ 'is-invalid': errors.date_of_birth }"
            />
            <div v-if="errors.date_of_birth" class="invalid-feedback">{{ errors.date_of_birth }}</div>
          </div>

          <div class="col-md-6">
            <label class="form-label">Contact Number</label>
            <input
              v-model="form.contact_number"
              class="form-control"
              placeholder="555-1234"
              :class="{ 'is-invalid': errors.contact_number }"
            />
            <div v-if="errors.contact_number" class="invalid-feedback">{{ errors.contact_number }}</div>
          </div>

          <div class="col-md-6">
            <label class="form-label">Address</label>
            <input v-model="form.address" class="form-control" />
          </div>

          <div class="col-md-6">
            <label class="form-label">Registration Date</label>
            <input
              type="date"
              v-model="form.registration_date"
              class="form-control"
              :class="{ 'is-invalid': errors.registration_date }"
            />
            <div v-if="errors.registration_date" class="invalid-feedback">{{ errors.registration_date }}</div>
          </div>

          <div class="col-md-6">
            <label class="form-label">Insurance Provider</label>
            <input v-model="form.insurance_provider" class="form-control" />
          </div>

          <div class="col-md-6">
            <label class="form-label">Insurance Number</label>
            <input v-model="form.insurance_number" class="form-control" />
          </div>

          <div class="col-md-6">
            <label class="form-label">Email</label>
            <input
              type="email"
              v-model="form.email"
              class="form-control"
              :class="{ 'is-invalid': errors.email }"
            />
            <div v-if="errors.email" class="invalid-feedback">{{ errors.email }}</div>
          </div>
        </div>

        <div class="text-center mt-4">
          <button type="submit" class="btn btn-primary px-4">Submit</button>
        </div>
      </form>

      <div v-if="message" class="alert alert-info mt-4 text-center">
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'NewPatient',
  data() {
    return {
      form: {
        patient_id: '',
        first_name: '',
        last_name: '',
        gender: '',
        date_of_birth: '',
        contact_number: '',
        address: '',
        registration_date: '',
        insurance_provider: '',
        insurance_number: '',
        email: ''
      },
      message: '',
      errors: {}
    }
  },
  methods: {
    validateForm() {
      this.errors = {}

      if (!this.form.patient_id) this.errors.patient_id = 'Patient ID is required.'
      if (!this.form.first_name) this.errors.first_name = 'First name is required.'
      if (!this.form.last_name) this.errors.last_name = 'Last name is required.'
      if (!this.form.gender) this.errors.gender = 'Gender is required.'
      if (!this.form.date_of_birth) this.errors.date_of_birth = 'Date of birth is required.'
      if (!this.form.contact_number) {
        this.errors.contact_number = 'Contact number is required.'
      } else if (!/^\+?[\d\s\-]{7,15}$/.test(this.form.contact_number)) {
        this.errors.contact_number = 'Invalid phone number format.'
      }
      if (!this.form.registration_date) this.errors.registration_date = 'Registration date is required.'
      if (this.form.email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        if (!emailRegex.test(this.form.email)) this.errors.email = 'Invalid email format.'
      }

      return Object.keys(this.errors).length === 0
    },

    async submitPatient() {
      if (!this.validateForm()) {
        this.message = 'Please fix errors before submitting.'
        return
      }
      this.message = ''
      try {
        const res = await axios.post('http://localhost:5000/patients', this.form)
        this.message = res.data.message || 'Patient registered successfully!'
        this.clearForm()
      } catch (err) {
        this.message = 'Error: ' + (err.response?.data?.message || err.message)
      }
    },

    clearForm() {
      this.form = {
        patient_id: '',
        first_name: '',
        last_name: '',
        gender: '',
        date_of_birth: '',
        contact_number: '',
        address: '',
        registration_date: '',
        insurance_provider: '',
        insurance_number: '',
        email: ''
      }
      this.errors = {}
    }
  }
}
</script>

<style scoped>
.form-control,
.form-select {
  max-width: 100%;
}

.is-invalid {
  border-color: #dc3545;
}

.invalid-feedback {
  color: #dc3545;
  font-size: 0.875em;
  margin-top: 0.25rem;
}
</style>
