<template>
  <div class="container my-5">
    <!-- Export Button -->
    <div class="text-end mb-3">
      <button class="btn btn-outline-danger" @click="exportPDF">📄 Export to PDF</button>
    </div>

    <!-- Report Content to Export -->
    <div class="card shadow-lg p-4" ref="reportContent">
      <h2 class="text-center text-primary mb-4">Billing Reports</h2>

      <div class="row">
        <!-- Summary -->
        <div class="col-md-12 mb-4">
          <h5 class="text-center">Total Revenue Summary</h5>
          <div class="row text-center">
            <div class="col-md-3">
              <div class="bg-light rounded p-3 shadow-sm">
                <strong>Total Revenue</strong>
                <div class="text-success h5">${{ totalRevenue.toFixed(2) }}</div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="bg-light rounded p-3 shadow-sm">
                <strong>Paid Bills</strong>
                <div class="text-primary h5">{{ paidCount }}</div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="bg-light rounded p-3 shadow-sm">
                <strong>Pending Bills</strong>
                <div class="text-warning h5">{{ pendingCount }}</div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="bg-light rounded p-3 shadow-sm">
                <strong>Cancelled Bills</strong>
                <div class="text-danger h5">{{ cancelledCount }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Monthly Revenue Chart -->
        <div class="col-md-6 mb-4 chart-container">
          <h5 class="text-center">Monthly Revenue</h5>
          <LineChart :chart-data="monthlyRevenueData" />
        </div>

        <!-- Unpaid Bills Table -->
        <div class="col-md-6 mb-4">
          <h5 class="text-center">Unpaid Bills List</h5>
          <table class="table table-sm table-bordered text-center">
            <thead class="table-light">
              <tr>
                <th>Bill ID</th>
                <th>Patient ID</th>
                <th>Amount</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="bill in unpaidBills" :key="bill.bill_id">
                <td>{{ bill.bill_id }}</td>
                <td>{{ bill.patient_id }}</td>
                <td>${{ bill.amount }}</td>
                <td>{{ bill.payment_status }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import html2pdf from 'html2pdf.js'
import LineChart from '../Charts/LineChart.vue'

export default {
  name: 'BillingReports',
  components: { LineChart },
  data() {
    return {
      billings: []
    }
  },
  computed: {
    totalRevenue() {
      return this.billings
        .filter(b => b.payment_status === 'Paid')
        .reduce((sum, b) => sum + parseFloat(b.amount || 0), 0)
    },
    paidCount() {
      return this.billings.filter(b => b.payment_status === 'Paid').length
    },
    pendingCount() {
      return this.billings.filter(b => b.payment_status === 'Pending').length
    },
    cancelledCount() {
      return this.billings.filter(b => b.payment_status === 'Cancelled').length
    },
    unpaidBills() {
      return this.billings.filter(b => b.payment_status !== 'Paid')
    },
    monthlyRevenueData() {
      const monthlyTotals = {}
      this.billings.forEach(b => {
        if (b.payment_status === 'Paid') {
          const month = b.bill_date?.slice(0, 7)
          if (month) {
            monthlyTotals[month] = (monthlyTotals[month] || 0) + parseFloat(b.amount || 0)
          }
        }
      })
      const labels = Object.keys(monthlyTotals).sort()
      const data = labels.map(m => monthlyTotals[m])
      return {
        labels,
        datasets: [
          {
            label: 'Revenue by Month',
            borderColor: '#4CAF50',
            backgroundColor: 'rgba(76, 175, 80, 0.2)',
            data
          }
        ]
      }
    }
  },
  methods: {
    async fetchBillings() {
      try {
        const response = await axios.get('http://localhost:5000/billing')
        this.billings = response.data
      } catch (error) {
        console.error('Error fetching billing data:', error.response?.data || error.message)
      }
    },
    exportPDF() {
      const element = this.$refs.reportContent
      const opt = {
        margin: [10, 10, 10, 10],
        filename: 'BillingReport.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: {
          scale: 3,
          useCORS: true,
          scrollY: 0
        },
        jsPDF: {
          unit: 'mm',
          format: 'a4',
          orientation: 'portrait'
        },
        pagebreak: {
          mode: ['avoid-all', 'css', 'legacy']
        }
      }

      html2pdf().set(opt).from(element).save()
    }
  },
  mounted() {
    this.fetchBillings()
  }
}
</script>

<style scoped>
h5 {
  font-weight: 600;
}
.pdf-wrapper {
  width: 100%;
  padding: 10px;
  background-color: white;
  font-size: 12px;
  line-height: 1.4;
}
canvas {
  max-width: 100% !important;
  height: auto !important;
}
.table {
  table-layout: auto;
  width: 100% !important;
  word-break: break-word;
  font-size: 12px;
}
.chart-container {
  max-height: 300px;
  overflow: hidden;
}
@media print {
  .row {
    display: block;
  }
  .col-md-6,
  .col-md-3,
  .col-md-12 {
    width: 100% !important;
    max-width: 100%;
    display: block;
  }
}
</style>
