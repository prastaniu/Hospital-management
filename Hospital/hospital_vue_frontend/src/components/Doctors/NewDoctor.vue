<template>
  <div class="d-flex justify-content-center my-5">
    <div class="card shadow-lg p-4" style="max-width: 900px; width: 100%;">

      <!-- Back Button -->
      <div class="mb-3">
        <router-link to="/doctors" class="btn btn-outline-secondary">
          ← Back
        </router-link>
      </div>

      <h2 class="mb-4 text-primary text-center">Add Doctor</h2>

      <form @submit.prevent="submitDoctor">
        <div class="row g-4">
          <!-- Doctor ID -->
          <div class="col-md-6">
            <div class="d-flex align-items-center">
              <label class="form-label mb-0 me-3" style="min-width: 160px;">Doctor ID</label>
              <input
                v-model="form.doctor_id"
                class="form-control"
                placeholder="DOC001"
                :class="{ 'is-invalid': errors.doctor_id }"
              />
            </div>
            <div v-if="errors.doctor_id" class="invalid-feedback">{{ errors.doctor_id }}</div>
          </div>

          <!-- First Name -->
          <div class="col-md-6">
            <div class="d-flex align-items-center">
              <label class="form-label mb-0 me-3" style="min-width: 160px;">First Name</label>
              <input
                v-model="form.first_name"
                class="form-control"
                :class="{ 'is-invalid': errors.first_name }"
              />
            </div>
            <div v-if="errors.first_name" class="invalid-feedback">{{ errors.first_name }}</div>
          </div>

          <!-- Last Name -->
          <div class="col-md-6">
            <div class="d-flex align-items-center">
              <label class="form-label mb-0 me-3" style="min-width: 160px;">Last Name</label>
              <input
                v-model="form.last_name"
                class="form-control"
                :class="{ 'is-invalid': errors.last_name }"
              />
            </div>
            <div v-if="errors.last_name" class="invalid-feedback">{{ errors.last_name }}</div>
          </div>

          <!-- Specialization -->
          <div class="col-md-6">
            <div class="d-flex align-items-center">
              <label class="form-label mb-0 me-3" style="min-width: 160px;">Specialization</label>
              <input
                v-model="form.specialization"
                class="form-control"
                placeholder="e.g., Cardiologist"
                :class="{ 'is-invalid': errors.specialization }"
              />
            </div>
            <div v-if="errors.specialization" class="invalid-feedback">{{ errors.specialization }}</div>
          </div>

          <!-- Phone Number -->
          <div class="col-md-6">
            <div class="d-flex align-items-center">
              <label class="form-label mb-0 me-3" style="min-width: 160px;">Phone Number</label>
              <input
                v-model="form.phone_number"
                class="form-control"
                :class="{ 'is-invalid': errors.phone_number }"
              />
            </div>
            <div v-if="errors.phone_number" class="invalid-feedback">{{ errors.phone_number }}</div>
          </div>

          <!-- Years of Experience -->
          <div class="col-md-6">
            <div class="d-flex align-items-center">
              <label class="form-label mb-0 me-3" style="min-width: 160px;">Experience (Years)</label>
              <input
                type="number"
                v-model.number="form.years_experience"
                class="form-control"
                min="0"
                :class="{ 'is-invalid': errors.years_experience }"
              />
            </div>
            <div v-if="errors.years_experience" class="invalid-feedback">{{ errors.years_experience }}</div>
          </div>

          <!-- Hospital Branch -->
          <div class="col-md-6">
            <div class="d-flex align-items-center">
              <label class="form-label mb-0 me-3" style="min-width: 160px;">Hospital Branch</label>
              <input
                v-model="form.hospital_branch"
                class="form-control"
                :class="{ 'is-invalid': errors.hospital_branch }"
              />
            </div>
            <div v-if="errors.hospital_branch" class="invalid-feedback">{{ errors.hospital_branch }}</div>
          </div>

          <!-- Email -->
          <div class="col-md-6">
            <div class="d-flex align-items-center">
              <label class="form-label mb-0 me-3" style="min-width: 160px;">Email</label>
              <input
                type="email"
                v-model="form.email"
                class="form-control"
                :class="{ 'is-invalid': errors.email }"
              />
            </div>
            <div v-if="errors.email" class="invalid-feedback">{{ errors.email }}</div>
          </div>
        </div>

        <div class="text-center mt-4">
          <button type="submit" class="btn btn-primary px-4">Submit</button>
        </div>
      </form>

      <div v-if="message" class="alert alert-info mt-3 text-center">
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'NewDoctor',
  data() {
    return {
      form: {
        doctor_id: '',
        first_name: '',
        last_name: '',
        specialization: '',
        phone_number: '',
        years_experience: '',
        hospital_branch: '',
        email: ''
      },
      message: '',
      errors: {}
    }
  },
  methods: {
    validateForm() {
      this.errors = {}

      if (!this.form.doctor_id) {
        this.errors.doctor_id = 'Doctor ID is required.'
      }

      if (!this.form.first_name) {
        this.errors.first_name = 'First name is required.'
      }

      if (!this.form.last_name) {
        this.errors.last_name = 'Last name is required.'
      }

      if (!this.form.specialization) {
        this.errors.specialization = 'Specialization is required.'
      }

      if (!this.form.phone_number) {
        this.errors.phone_number = 'Phone number is required.'
      } else if (!/^\+?[\d\s\-]{7,15}$/.test(this.form.phone_number)) {
        this.errors.phone_number = 'Phone number format is invalid.'
      }

      if (this.form.years_experience === '' || this.form.years_experience === null) {
        this.errors.years_experience = 'Years of experience is required.'
      } else if (this.form.years_experience < 0) {
        this.errors.years_experience = 'Years of experience cannot be negative.'
      }

      if (!this.form.hospital_branch) {
        this.errors.hospital_branch = 'Hospital branch is required.'
      }

      if (!this.form.email) {
        this.errors.email = 'Email is required.'
      } else if (
        !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.form.email)
      ) {
        this.errors.email = 'Email format is invalid.'
      }

      return Object.keys(this.errors).length === 0
    },

    async submitDoctor() {
      if (!this.validateForm()) {
        this.message = 'Please fix the errors before submitting.'
        return
      }

      this.message = ''
      try {
        const res = await axios.post('http://localhost:5000/doctors', this.form)
        this.message = res.data.message || 'Doctor added successfully!'
        this.clearForm()
      } catch (err) {
        this.message = 'Error: ' + (err.response?.data?.message || err.message)
      }
    },

    clearForm() {
      this.form = {
        doctor_id: '',
        first_name: '',
        last_name: '',
        specialization: '',
        phone_number: '',
        years_experience: '',
        hospital_branch: '',
        email: ''
      }
      this.errors = {}
    }
  }
}
</script>

<style scoped>
.form-control {
  max-width: 280px;
}

.is-invalid {
  border-color: #dc3545;
}

.invalid-feedback {
  color: #dc3545;
  font-size: 0.875em;
  margin-top: 0.25rem;
  max-width: 280px;
  margin-left: auto;
  margin-right: auto;
}
</style>
