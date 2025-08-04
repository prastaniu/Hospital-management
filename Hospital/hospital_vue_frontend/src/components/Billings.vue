<template>
  <div class="container my-5">
    <div class="card shadow-lg p-4">
      <h2 class="text-center text-primary mb-4">Billing Records</h2>

      <div class="text-end mb-3">
        <router-link to="/" class="btn btn-outline-secondary">← Back to Home</router-link>
      </div>

      <div v-if="loading" class="text-center">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-else>
        <table class="table table-striped table-bordered">
          <thead class="table-dark">
            <tr>
              <th>Bill ID</th>
              <th>Patient ID</th>
              <th>Treatment ID</th>
              <th>Bill Date</th>
              <th>Amount ($)</th>
              <th>Method</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="bill in billings" :key="bill.bill_id">
              <td>{{ bill.bill_id }}</td>
              <td>{{ bill.patient_id }}</td>
              <td>{{ bill.treatment_id }}</td>
              <td>{{ formatDate(bill.bill_date) }}</td>
              <td>{{ Number(bill.amount).toFixed(2) }}</td>
              <td>{{ bill.payment_method }}</td>
              <td>{{ bill.payment_status }}</td>
              <td>
                <button class="btn btn-sm btn-primary" @click="openEditModal(bill)">Edit</button>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="billings.length === 0" class="alert alert-info text-center">
          No billing records found.
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="showModal" class="modal-backdrop">
      <div class="modal-card card shadow p-4">
        <h5 class="text-center mb-3">Update Billing - {{ selectedBill.bill_id }}</h5>

        <div class="mb-3">
          <label class="form-label">Payment Method</label>
          <select class="form-control" v-model="selectedBill.payment_method">
            <option>Cash</option>
            <option>Credit Card</option>
            <option>Insurance</option>
            <option>Online</option>
          </select>
        </div>

        <div class="mb-3">
          <label class="form-label">Payment Status</label>
          <select class="form-control" v-model="selectedBill.payment_status">
            <option>Unpaid</option>
            <option>Pending</option>
            <option>Partially Paid</option>
            <option>Paid</option>
          </select>
        </div>

        <div class="text-end">
          <button class="btn btn-secondary me-2" @click="closeModal">Cancel</button>
          <button class="btn btn-success" @click="updateBilling">Update</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Billings',
  data() {
    return {
      billings: [],         // initialize empty array
      loading: true,
      showModal: false,
      selectedBill: {}
    }
  },
  methods: {
    async fetchBillings() {
      try {
        const res = await axios.get('http://localhost:5000/billing')
        this.billings = res.data
      } catch (error) {
        console.error('Error fetching billing records:', error)
      } finally {
        this.loading = false
      }
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString()
    },
    openEditModal(bill) {
      this.selectedBill = { ...bill } // clone to avoid direct binding
      this.showModal = true
    },
    closeModal() {
      this.showModal = false
      this.selectedBill = {}
    },
    async updateBilling() {
      try {
        await axios.put(`http://localhost:5000/billing/${this.selectedBill.bill_id}`, {
          payment_method: this.selectedBill.payment_method,
          payment_status: this.selectedBill.payment_status
        })
        this.closeModal()
        this.fetchBillings()
      } catch (error) {
        console.error('Error updating billing record:', error)
      }
    }
  },
  mounted() {
    this.fetchBillings()
  }
}
</script>

<style scoped>
.table th,
.table td {
  vertical-align: middle;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-card {
  width: 100%;
  max-width: 400px;
  background: white;
  border-radius: 10px;
}
</style>
