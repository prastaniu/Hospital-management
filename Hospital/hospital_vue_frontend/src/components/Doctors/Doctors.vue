<template>
  <div class="container my-5">
    <div class="card shadow-lg p-4" style="max-width: 900px; margin: auto;">
      <h2 class="text-center text-primary mb-4">
        {{ showAddForm ? 'Add Doctor' : 'Doctors List' }}
      </h2>

      <div v-if="!showAddForm" class="text-end mb-3">
        <button class="btn btn-success" @click="toggleAddForm(true)">
          + Add New Doctor
        </button>
      </div>
      <div v-else class="mb-3">
        <button class="btn btn-outline-secondary" @click="toggleAddForm(false)">
          ← Back to Doctors List
        </button>
      </div>

      <!-- Doctors List -->
      <div v-if="!showAddForm">
        <table class="table table-bordered table-hover text-center">
          <thead class="table-light">
            <tr>
              <th>Doctor ID</th>
              <th>Name</th>
              <th>Specialization</th>
              <th>Phone</th>
              <th>Experience</th>
              <th>Branch</th>
              <th>Email</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="doc in doctors" :key="doc.doctor_id">
              <td>{{ doc.doctor_id }}</td>
              <td>{{ doc.first_name }} {{ doc.last_name }}</td>
              <td>{{ doc.specialization }}</td>
              <td>{{ doc.phone_number }}</td>
              <td>{{ doc.years_experience }} yrs</td>
              <td>{{ doc.hospital_branch }}</td>
              <td>{{ doc.email }}</td>
              <td>
                <div class="btn-group">
                  <button class="btn btn-sm btn-edit" @click="editDoctor(doc)">Edit</button>
                  <button class="btn btn-sm btn-danger" @click="deleteDoctor(doc.doctor_id)"
                    :disabled="hasAppointments(doc.doctor_id)">
                    Delete
                  </button>
                </div>
              </td>

            </tr>
          </tbody>
        </table>

        <!-- Edit Modal -->
        <div v-if="selectedDoctor" class="modal d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.4);">
          <div class="modal-dialog">
            <div class="modal-content p-3">
              <h5 class="modal-title">Edit Doctor</h5>
              <form @submit.prevent="updateDoctor">
                <div class="mb-2" v-for="(value, key) in selectedDoctor" :key="key" v-if="key !== 'doctor_id'">
                  <label class="form-label text-capitalize">{{ key.replace('_', ' ') }}</label>
                  <input v-model="selectedDoctor[key]" :class="['form-control', errors[key] ? 'is-invalid' : '']"
                    :type="key === 'email' ? 'email' : 'text'" />
                  <div v-if="errors[key]" class="invalid-feedback">{{ errors[key] }}</div>
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

      <!-- Add New Doctor Form -->
      <div v-else>
        <form @submit.prevent="submitDoctor">
          <div class="row g-4">
            <div class="col-md-6" v-for="field in formFields" :key="field.key">
              <div class="d-flex align-items-center">
                <label class="form-label mb-0 me-3" style="min-width: 160px;">{{ field.label }}</label>
                <input v-model="form[field.key]" :type="field.type || 'text'" class="form-control"
                  :placeholder="field.placeholder || ''" :class="{ 'is-invalid': errors[field.key] }"
                  :min="field.min" />
              </div>
              <div v-if="errors[field.key]" class="invalid-feedback">{{ errors[field.key] }}</div>
            </div>
          </div>

          <div class="text-center mt-4">
            <button type="submit" class="btn btn-primary px-4">Submit</button>
          </div>
        </form>

        <div v-if="message" class="alert alert-info mt-3 text-center">{{ message }}</div>
      </div>

      <div v-if="message && !showAddForm" class="alert alert-info mt-4 text-center">{{ message }}</div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Doctors",
  data() {
    return {
      message: "",
      selectedDoctor: null,
      errors: {},
      doctors: [],
      appointments: [],
      showAddForm: false,
      form: {
        doctor_id: "",
        first_name: "",
        last_name: "",
        specialization: "",
        phone_number: "",
        years_experience: "",
        hospital_branch: "",
        email: "",
      },
      formFields: [
        { key: "doctor_id", label: "Doctor ID" },
        { key: "first_name", label: "First Name" },
        { key: "last_name", label: "Last Name" },
        { key: "specialization", label: "Specialization" },
        { key: "phone_number", label: "Phone Number" },
        { key: "years_experience", label: "Experience (Years)", type: "number", min: 0 },
        { key: "hospital_branch", label: "Hospital Branch" },
        { key: "email", label: "Email", type: "email" },
      ],
    };
  },
  mounted() {
    this.fetchDoctors();
    this.fetchAppointments();
  },
  methods: {
    toggleAddForm(val) {
      this.showAddForm = val;
      this.message = "";
      this.errors = {};
      this.selectedDoctor = null;
      if (val === false) this.fetchDoctors();
    },
    editDoctor(doctor) {
      this.selectedDoctor = { ...doctor };
      this.errors = {};
      this.message = "";
    },
    validateEmail(email) {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return re.test(email);
    },
    validateDoctor() {
      this.errors = {};
      const d = this.selectedDoctor;

      if (!d.first_name || !d.first_name.trim()) this.errors.first_name = "First name is required.";
      if (!d.last_name || !d.last_name.trim()) this.errors.last_name = "Last name is required.";
      if (!d.specialization || !d.specialization.trim()) this.errors.specialization = "Specialization is required.";
      if (!d.phone_number || !d.phone_number.trim()) this.errors.phone_number = "Phone number is required.";
      if (
        d.years_experience === null ||
        d.years_experience === undefined ||
        d.years_experience === "" ||
        isNaN(d.years_experience) ||
        !Number.isInteger(Number(d.years_experience)) ||
        Number(d.years_experience) < 0
      ) {
        this.errors.years_experience = "Years of experience must be a non-negative integer.";
      }
      if (!d.hospital_branch || !d.hospital_branch.trim()) this.errors.hospital_branch = "Hospital branch is required.";
      if (d.email && d.email.trim() && !this.validateEmail(d.email.trim())) this.errors.email = "Invalid email format.";

      return Object.keys(this.errors).length === 0;
    },
    validateForm() {
      this.errors = {};

      if (!this.form.doctor_id) this.errors.doctor_id = "Doctor ID is required.";
      if (!this.form.first_name) this.errors.first_name = "First name is required.";
      if (!this.form.last_name) this.errors.last_name = "Last name is required.";
      if (!this.form.specialization) this.errors.specialization = "Specialization is required.";
      if (!this.form.phone_number) this.errors.phone_number = "Phone number is required.";
      else if (!/^\+?[\d\s\-]{7,15}$/.test(this.form.phone_number)) this.errors.phone_number = "Phone number format is invalid.";
      if (this.form.years_experience === "" || this.form.years_experience === null)
        this.errors.years_experience = "Years of experience is required.";
      else if (this.form.years_experience < 0) this.errors.years_experience = "Years of experience cannot be negative.";
      if (!this.form.hospital_branch) this.errors.hospital_branch = "Hospital branch is required.";
      if (!this.form.email) this.errors.email = "Email is required.";
      else if (!this.validateEmail(this.form.email)) this.errors.email = "Email format is invalid.";

      return Object.keys(this.errors).length === 0;
    },
    fetchDoctors() {
      axios
        .get("http://127.0.0.1:5000/doctors")
        .then((res) => {
          this.doctors = res.data;
        })
        .catch((err) => {
          console.error(err);
          this.message = "Failed to load doctors.";
        });
    },
    fetchAppointments() {
      axios
        .get("http://127.0.0.1:5000/appointments")
        .then((res) => {
          this.appointments = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    hasAppointments(doctorId) {
      return this.appointments.some((appt) => appt.doctor_id === doctorId);
    },
    updateDoctor() {
      if (!this.validateDoctor()) {
        this.message = "Please fix validation errors before saving.";
        return;
      }

      axios
        .put(`http://127.0.0.1:5000/doctors/${this.selectedDoctor.doctor_id}`, this.selectedDoctor)
        .then(() => {
          this.fetchDoctors();
          this.message = "Doctor updated successfully.";
          this.selectedDoctor = null;
          this.errors = {};
        })
        .catch((err) => {
          console.error(err);
          this.message = "Failed to update doctor.";
        });
    },
    async submitDoctor() {
      if (!this.validateForm()) {
        this.message = "Please fix the errors before submitting.";
        return;
      }

      this.message = "";
      try {
        const res = await axios.post("http://127.0.0.1:5000/doctors", this.form);
        this.message = res.data.message || "Doctor added successfully!";
        this.clearForm();
        this.toggleAddForm(false);
      } catch (err) {
        this.message = "Error: " + (err.response?.data?.message || err.message);
      }
    },
    clearForm() {
      this.form = {
        doctor_id: "",
        first_name: "",
        last_name: "",
        specialization: "",
        phone_number: "",
        years_experience: "",
        hospital_branch: "",
        email: "",
      };
      this.errors = {};
    },
    deleteDoctor(id) {
      axios
        .delete(`http://127.0.0.1:5000/doctors/${id}`)
        .then(() => {
          this.fetchDoctors();
          this.message = "Doctor deleted successfully.";
        })
        .catch((err) => {
          console.error(err);
          this.message =
            err.response?.data?.message || "Failed to delete doctor. It may have appointments associated.";
        });
    },
    cancelEdit() {
      this.selectedDoctor = null;
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
  overflow-y: auto;
  background-color: rgba(0, 0, 0, 0.4);
  z-index: 1050;
}

.modal-dialog {
  margin-top: 10%;
  max-width: 500px;
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

/* Buttons container so buttons stay side by side */
.btn-group {
  display: flex;
  gap: 0.5rem;
  /* space between buttons */
  justify-content: center;
  /* center in cell */
}

/* Override btn-warning and btn-danger with your main project colors */
.btn-edit {
  background-color: #1a73e8;
  /* example blue */
  border-color: #1a73e8;
  color: white;
}

.btn-edit:hover {
  background-color: #155ab6;
  border-color: #155ab6;
}

.btn-delete {
  background-color: #e53935;
  /* example red */
  border-color: #e53935;
  color: white;
}

.btn-delete:hover {
  background-color: #ab2c26;
  border-color: #ab2c26;
}
</style>
