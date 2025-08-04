<template>
  <div class="container my-5">
    <div class="card shadow-lg p-4">
      <h2 class="text-center text-primary mb-4">Appointments List</h2>

      <div class="text-end mb-3">
        <router-link to="/new-appointment" class="btn btn-success">
          + Add New Appointment
        </router-link>
      </div>

      <table class="table table-bordered table-hover text-center">
        <thead class="table-light">
          <tr>
            <th>Appointment ID</th>
            <th>Patient ID</th>
            <th>Doctor</th>
            <th>Date</th>
            <th>Time</th>
            <th>Reason</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="appt in appointments" :key="appt.appointment_id">
            <td>{{ appt.appointment_id }}</td>
            <td>{{ appt.patient_id }}</td>
            <td>{{ getDoctorName(appt.doctor_id) }}</td>
            <td>{{ appt.appointment_date }}</td>
            <td>{{ appt.appointment_time }}</td>
            <td>{{ appt.reason_for_visit }}</td>
            <td>{{ appt.status }}</td>
            <td>
              <button class="btn btn-sm btn-primary me-2" @click="editAppointment(appt)">Edit</button>
              <button class="btn btn-sm btn-danger" @click="deleteAppointment(appt.appointment_id)"
                :disabled="appt.status === 'Cancelled' || appt.status === 'Completed' || appt.has_treatment"
                :title="appt.has_treatment ? 'Appointment has related treatments' : 'Delete appointment'">
                Delete
              </button>

            </td>
          </tr>
        </tbody>
      </table>

      <!-- Edit Modal -->
      <div v-if="selectedAppointment" class="modal d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.4);">
        <div class="modal-dialog">
          <div class="modal-content p-3">
            <h5 class="modal-title">Edit Appointment</h5>
            <div class="modal-body">
              <form @submit.prevent="updateAppointment">
                <div class="mb-2">
                  <label class="form-label">Patient ID</label>
                  <input v-model="selectedAppointment.patient_id"
                    :class="['form-control', errors.patient_id ? 'is-invalid' : '']" />
                  <div v-if="errors.patient_id" class="invalid-feedback">{{ errors.patient_id }}</div>
                </div>

                <div class="mb-2">
                  <label class="form-label">Doctor</label>
                  <select v-model="selectedAppointment.doctor_id"
                    :class="['form-select', errors.doctor_id ? 'is-invalid' : '']">
                    <option value="">-- Select Doctor --</option>
                    <option v-for="doc in doctors" :key="doc.doctor_id" :value="doc.doctor_id">
                      {{ doc.name }}
                    </option>
                  </select>
                  <div v-if="errors.doctor_id" class="invalid-feedback">{{ errors.doctor_id }}</div>
                </div>

                <div class="mb-2">
                  <label class="form-label">Date</label>
                  <input type="date" v-model="selectedAppointment.appointment_date"
                    :class="['form-control', errors.appointment_date ? 'is-invalid' : '']" />
                  <div v-if="errors.appointment_date" class="invalid-feedback">{{ errors.appointment_date }}</div>
                </div>

                <div class="mb-2">
                  <label class="form-label">Time</label>
                  <input type="time" v-model="selectedAppointment.appointment_time"
                    :class="['form-control', errors.appointment_time ? 'is-invalid' : '']" />
                  <div v-if="errors.appointment_time" class="invalid-feedback">{{ errors.appointment_time }}</div>
                </div>

                <div class="mb-2">
                  <label class="form-label">Reason</label>
                  <input v-model="selectedAppointment.reason_for_visit"
                    :class="['form-control', errors.reason_for_visit ? 'is-invalid' : '']" />
                  <div v-if="errors.reason_for_visit" class="invalid-feedback">{{ errors.reason_for_visit }}</div>
                </div>

                <div class="mb-2">
                  <label class="form-label">Status</label>
                  <select v-model="selectedAppointment.status"
                    :class="['form-select', errors.status ? 'is-invalid' : '']">
                    <option value="Scheduled">Scheduled</option>
                    <option value="Completed">Completed</option>
                    <option value="Cancelled">Cancelled</option>
                  </select>
                  <div v-if="errors.status" class="invalid-feedback">{{ errors.status }}</div>
                </div>

                <div class="mt-3 text-end">
                  <button class="btn btn-secondary me-2" @click.prevent="cancelEdit">Cancel</button>
                  <button class="btn btn-primary" type="submit">Save</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>

      <div v-if="message" class="alert alert-info mt-4 text-center">{{ message }}</div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "Appointments",
  data() {
    return {
      message: "",
      selectedAppointment: null,
      errors: {},
      doctors: [],
      appointments: [],
    };
  },
  mounted() {
    this.fetchDoctors();
    this.fetchAppointments();
  },
  methods: {
    getDoctorName(doctorId) {
      const doc = this.doctors.find((d) => d.doctor_id === doctorId);
      return doc ? doc.name : "Unknown";
    },
    editAppointment(appt) {
      this.selectedAppointment = { ...appt };
      this.errors = {};
      this.message = "";
    },
    validateAppointment() {
      const a = this.selectedAppointment;
      this.errors = {};
      if (!a.patient_id?.trim()) this.errors.patient_id = "Patient ID is required.";
      if (!a.doctor_id) this.errors.doctor_id = "Doctor must be selected.";
      if (!a.appointment_date) this.errors.appointment_date = "Appointment date is required.";
      if (!a.appointment_time) this.errors.appointment_time = "Appointment time is required.";
      if (!a.reason_for_visit?.trim()) this.errors.reason_for_visit = "Reason is required.";
      if (!["Scheduled", "Completed", "Cancelled"].includes(a.status)) {
        this.errors.status = "Status must be valid.";
      }
      return Object.keys(this.errors).length === 0;
    },
    async fetchDoctors() {
      try {
        const res = await axios.get("http://127.0.0.1:5000/doctors");
        this.doctors = res.data.map(doc => ({
          ...doc,
          name: `${doc.first_name} ${doc.last_name}`
        }));
      } catch {
        this.message = "Error loading doctors.";
      }
    },
    async fetchAppointments() {
      try {
        const res = await axios.get("http://127.0.0.1:5000/appointments");
        this.appointments = res.data;
      } catch {
        this.message = "Error fetching appointments.";
      }
    },
    async updateAppointment() {
      if (!this.validateAppointment()) {
        this.message = "Fix errors before saving.";
        return;
      }
      try {
        const res = await axios.put(
          `http://127.0.0.1:5000/appointments/${this.selectedAppointment.appointment_id}`,
          this.selectedAppointment
        );
        this.message = res.data.message || "Appointment updated.";
        this.selectedAppointment = null;
        this.fetchAppointments();
      } catch (err) {
        this.message = "Error updating appointment.";
      }
    },
    async deleteAppointment(id) {
      if (!confirm("Are you sure you want to delete this appointment?")) return;
      try {
        const encodedId = encodeURIComponent(id);
        const res = await axios.delete(`http://127.0.0.1:5000/appointments/${encodedId}`);
        this.message = res.data.message || "Appointment deleted.";
        this.fetchAppointments();
      } catch (err) {
        console.error("Delete failed:", err);
        this.message = "Error deleting appointment.";
      }
    }
    ,
    cancelEdit() {
      this.selectedAppointment = null;
      this.errors = {};
      this.message = "";
    },
  },
};
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

.is-invalid {
  border-color: #dc3545;
}

.invalid-feedback {
  color: #dc3545;
  font-size: 0.875em;
  margin-top: 0.25rem;
}
</style>
