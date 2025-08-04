<template>
  <div class="container my-5">
    <div class="card shadow-lg p-4">
      <h2 class="text-center text-primary mb-4">Patients List</h2>

      <div class="d-flex justify-content-end mb-3">
        <router-link to="/new-patient" class="btn btn-success">
          + Add New Patient
        </router-link>
      </div>

      <table class="table table-bordered table-hover text-center">
        <thead class="table-light">
          <tr>
            <th>Patient ID</th>
            <th>Name</th>
            <th>Gender</th>
            <th>DOB</th>
            <th>Contact</th>
            <th>Insurance</th>
            <th>Email</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="pat in patients" :key="pat.patient_id">
            <td>{{ pat.patient_id }}</td>
            <td>{{ pat.first_name }} {{ pat.last_name }}</td>
            <td>{{ pat.gender }}</td>
            <td>{{ pat.date_of_birth }}</td>
            <td>{{ pat.contact_number }}</td>
            <td>{{ pat.insurance_provider }}</td>
            <td>{{ pat.email }}</td>
            <td>
              <button class="btn btn-sm btn-warning me-2" @click="editPatient(pat)">Edit</button>
              <button class="btn btn-sm btn-danger" @click="deletePatient(pat.patient_id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Edit Modal -->
      <div v-if="selectedPatient" class="modal d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.4);">
        <div class="modal-dialog">
          <div class="modal-content p-3">
            <h5 class="modal-title">Edit Patient</h5>
            <form @submit.prevent="updatePatient">
              <div v-for="(value, key) in selectedPatient" :key="key" class="mb-2" v-if="key !== 'patient_id'">
                <label class="form-label text-capitalize">
                  {{ key.replace('_', ' ') }}
                  <span class="text-danger" v-if="['first_name','last_name','gender','date_of_birth','contact_number'].includes(key)">*</span>
                </label>

                <!-- Gender Dropdown -->
                <select v-if="key === 'gender'"
                        v-model="selectedPatient[key]"
                        class="form-select"
                        :class="{ 'is-invalid': errors[key] }">
                  <option value="">Select Gender</option>
                  <option value="M">Male</option>
                  <option value="F">Female</option>
                  <option value="O">Other</option>
                </select>

                <!-- Other Inputs -->
                <input v-else
                       v-model="selectedPatient[key]"
                       :class="['form-control', errors[key] ? 'is-invalid' : '']"
                       :type="key.includes('date') ? 'date' : key === 'email' ? 'email' : 'text'" />

                <div v-if="errors[key]" class="invalid-feedback">{{ errors[key] }}</div>
              </div>

              <div class="text-end mt-3">
                <button class="btn btn-secondary me-2" @click.prevent="cancelEdit">Cancel</button>
                <button class="btn btn-primary" type="submit">Save</button>
              </div>
            </form>
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
  name: "Patients",
  data() {
    return {
      message: "",
      selectedPatient: null,
      errors: {},
      patients: [],
    };
  },
  mounted() {
    this.fetchPatients();
  },
  methods: {
    async fetchPatients() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/patients");
        this.patients = response.data;
      } catch (error) {
        console.error("Error fetching patients:", error);
        this.message = "Failed to load patient data from API.";
      }
    },
    formatDate(value) {
      const d = new Date(value);
      return d.toISOString().split("T")[0];
    },
    editPatient(patient) {
      const copy = { ...patient };
      if (copy.date_of_birth) copy.date_of_birth = this.formatDate(copy.date_of_birth);
      if (copy.registration_date) copy.registration_date = this.formatDate(copy.registration_date);
      this.selectedPatient = copy;
      this.errors = {};
      this.message = "";
    },
    validateEmail(email) {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return re.test(email);
    },
    validateDate(date) {
      return !isNaN(Date.parse(date));
    },
    validatePatient() {
      this.errors = {};
      const p = this.selectedPatient;

      if (!p.first_name?.trim()) this.errors.first_name = "First name is required.";
      if (!p.last_name?.trim()) this.errors.last_name = "Last name is required.";
      if (!p.gender?.trim()) {
        this.errors.gender = "Gender is required.";
      } else if (!['M', 'F', 'O'].includes(p.gender.trim().toUpperCase())) {
        this.errors.gender = "Gender must be M, F, or O.";
      }
      if (!p.date_of_birth || !this.validateDate(p.date_of_birth)) {
        this.errors.date_of_birth = "Valid date of birth is required.";
      }
      if (!p.contact_number?.trim()) this.errors.contact_number = "Contact number is required.";
      if (p.email && !this.validateEmail(p.email)) this.errors.email = "Invalid email format.";
      if (p.registration_date && !this.validateDate(p.registration_date)) {
        this.errors.registration_date = "Valid registration date is required.";
      }

      return Object.keys(this.errors).length === 0;
    },
    async updatePatient() {
      if (!this.validatePatient()) {
        this.message = "Please fix validation errors before saving.";
        return;
      }

      this.selectedPatient.gender = this.selectedPatient.gender.trim().toUpperCase();

      try {
        const res = await axios.put(
          `http://127.0.0.1:5000/patients/${this.selectedPatient.patient_id}`,
          this.selectedPatient
        );
        this.message = res.data.message || "Patient updated successfully.";
        this.selectedPatient = null;
        this.fetchPatients();
      } catch (error) {
        console.error("Error updating patient:", error);
        this.message = "Failed to update patient.";
      }
    },
    async deletePatient(id) {
      if (!confirm("Are you sure you want to delete this patient?")) return;

      try {
        await axios.delete(`http://127.0.0.1:5000/patients/${id}`);
        this.message = "Patient deleted successfully.";
        this.fetchPatients();
      } catch (error) {
        console.error("Error deleting patient:", error);
        this.message = "Failed to delete patient.";
      }
    },
    cancelEdit() {
      this.selectedPatient = null;
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
