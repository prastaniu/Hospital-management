<template>
  <div class="d-flex justify-content-center my-5">
    <div class="card shadow-lg p-4" style="max-width: 900px; width: 100%;">
      <!-- Back Button -->
      <div class="mb-3">
        <router-link to="/appointments" class="btn btn-outline-secondary">
          ← Back
        </router-link>
      </div>

      <h2 class="mb-4 text-primary text-center">Book an Appointment</h2>

      <form @submit.prevent="submitAppointment">
        <div class="row g-4">
          <div class="col-md-6">
            <div class="d-flex align-items-center">
              <label class="form-label mb-0 me-3" style="min-width: 140px;">Appointment ID</label>
              <input v-model="form.appointment_id" class="form-control"  />
            </div>
          </div>

          <div class="col-md-6">
            <div class="d-flex align-items-center">
              <label class="form-label mb-0 me-3" style="min-width: 140px;">Patient ID</label>
              <input
                v-model="form.patient_id"
                class="form-control"
                placeholder="PAT123"
                :class="{ 'is-invalid': errors.patient_id }"
              />
            </div>
            <div v-if="errors.patient_id" class="invalid-feedback">{{ errors.patient_id }}</div>
          </div>

          <div class="col-md-6">
            <div class="d-flex align-items-center">
              <label class="form-label mb-0 me-3" style="min-width: 140px;">Doctor</label>
              <select
                v-model="form.doctor_id"
                class="form-select"
                :class="{ 'is-invalid': errors.doctor_id }"
              >
                <option disabled value="">Select a doctor</option>
                <option v-for="doc in doctors" :key="doc.doctor_id" :value="doc.doctor_id">
                  {{ doc.name }}
                </option>
              </select>
            </div>
            <div v-if="errors.doctor_id" class="invalid-feedback">{{ errors.doctor_id }}</div>
          </div>

          <div class="col-md-6">
            <div class="d-flex align-items-center">
              <label class="form-label mb-0 me-3" style="min-width: 140px;">Date</label>
              <input
                type="date"
                v-model="form.appointment_date"
                class="form-control"
                :class="{ 'is-invalid': errors.appointment_date }"
              />
            </div>
            <div v-if="errors.appointment_date" class="invalid-feedback">{{ errors.appointment_date }}</div>
          </div>

          <div class="col-md-6">
            <div class="d-flex align-items-center">
              <label class="form-label mb-0 me-3" style="min-width: 140px;">Time</label>
              <input
                type="time"
                v-model="form.appointment_time"
                class="form-control"
                :class="{ 'is-invalid': errors.appointment_time }"
              />
            </div>
            <div v-if="errors.appointment_time" class="invalid-feedback">{{ errors.appointment_time }}</div>
          </div>

          <div class="col-md-6">
            <div class="d-flex align-items-center">
              <label class="form-label mb-0 me-3" style="min-width: 140px;">Reason</label>
              <input
                v-model="form.reason_for_visit"
                class="form-control"
                placeholder="e.g., Fever"
                :class="{ 'is-invalid': errors.reason_for_visit }"
              />
            </div>
            <div v-if="errors.reason_for_visit" class="invalid-feedback">{{ errors.reason_for_visit }}</div>
          </div>

          <div class="col-md-6">
            <div class="d-flex align-items-center">
              <label class="form-label mb-0 me-3" style="min-width: 140px;">Status</label>
              <select
                v-model="form.status"
                class="form-select"
                :class="{ 'is-invalid': errors.status }"
              >
                <option value="">Select status</option>
                <option value="Scheduled">Scheduled</option>
                <option value="Completed">Completed</option>
                <option value="Cancelled">Cancelled</option>
              </select>
            </div>
            <div v-if="errors.status" class="invalid-feedback">{{ errors.status }}</div>
          </div>
        </div>

        <div class="text-center mt-4">
          <button type="submit" class="btn btn-primary px-4">Submit</button>
        </div>
      </form>

      <div v-if="message" class="alert alert-info mt-3 text-center">
        {{ message }}
      </div>

      <!-- Fetched Appointments Table -->
      <h3 class="mt-5 text-center text-secondary">Existing Appointments</h3>
      <table class="table table-bordered mt-3">
        <thead>
          <tr class="table-light text-center">
            <th>Appointment ID</th>
            <th>Patient ID</th>
            <th>Doctor ID</th>
            <th>Date</th>
            <th>Time</th>
            <th>Reason</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="appt in appointments" :key="appt.appointment_id" class="text-center">
            <td>{{ appt.appointment_id }}</td>
            <td>{{ appt.patient_id }}</td>
            <td>{{ appt.doctor_id }}</td>
            <td>{{ appt.appointment_date }}</td>
            <td>{{ appt.appointment_time }}</td>
            <td>{{ appt.reason_for_visit }}</td>
            <td>{{ appt.status }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'NewAppointment',
  data() {
    return {
      form: {
        appointment_id: '',
        patient_id: '',
        doctor_id: '',
        appointment_date: '',
        appointment_time: '',
        reason_for_visit: '',
        status: ''
      },
      message: '',
      errors: {},
      doctors: [],
      appointments: []
    }
  },
  mounted() {
    //this.generateAppointmentId()
    this.fetchDoctors()
    this.fetchAppointments()
  },
  methods: {
    generateAppointmentId() {
      const today = new Date()
      const dateStr = today.toISOString().slice(0, 10).replace(/-/g, '')
      const randomNum = Math.floor(100 + Math.random() * 900)
      this.form.appointment_id = `APT-${randomNum}`
    },
   /*  async fetchDoctors() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/doctors')
        this.doctors = res.data
      } catch {
        this.message = 'There is no doctors available at this time'
      }
    }, */
    async fetchDoctors() {
  try {
    const res = await axios.get("http://127.0.0.1:5000/doctors");
    this.doctors = res.data.map(doc => ({
      ...doc,
      name: `${doc.first_name} ${doc.last_name}`,
    }));
  } catch {
    this.message = "There is no doctors available at this time";
  }
},

    async fetchAppointments() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/appointments')
        this.appointments = res.data
      } catch (err) {
        this.message = 'Error fetching appointments.'
      }
    },
    validateForm() {
      this.errors = {}

      if (!this.form.patient_id) this.errors.patient_id = 'Patient ID is required.'
      if (!this.form.doctor_id) this.errors.doctor_id = 'Doctor selection is required.'
      if (!this.form.appointment_date) this.errors.appointment_date = 'Appointment date is required.'
      if (!this.form.appointment_time) this.errors.appointment_time = 'Appointment time is required.'
      if (!this.form.reason_for_visit) this.errors.reason_for_visit = 'Reason for visit is required.'
      if (!this.form.status) this.errors.status = 'Status is required.'

      return Object.keys(this.errors).length === 0
    },
    async submitAppointment() {
      if (!this.validateForm()) {
        this.message = 'Please fix the errors before submitting.'
        return
      }

      this.message = ''

      try {
        const res = await axios.post('http://127.0.0.1:5000/appointments', this.form)
        this.message = res.data.message || 'Appointment created!'
        this.clearForm()
        this.fetchAppointments()
      } catch (err) {
        this.message = 'Error: ' + (err.response?.data?.message || err.message)
      }
    },
    clearForm() {
      this.form = {
        appointment_id: '',
        patient_id: '',
        doctor_id: '',
        appointment_date: '',
        appointment_time: '',
        reason_for_visit: '',
        status: ''
      }
      this.generateAppointmentId()
    }
  }
}
</script>

<style scoped>
.form-control,
.form-select {
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
