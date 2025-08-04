import { createRouter, createWebHistory } from 'vue-router'
import Home from './components/Home.vue'

import AuthPage from './components/User/AuthPage.vue'
import Login from './components/User/LoginPage.vue'
import Register from './components/User/RegisterPage.vue'

import Patients from './components/Patients/Patients.vue'
import NewPatient from './components/Patients/NewPatient.vue'

import Doctors from './components/Doctors/Doctors.vue'
import NewDoctor from './components/Doctors/NewDoctor.vue'

import NewAppointment from './components/Appointments/NewAppointment.vue'
import Appointments from './components/Appointments/Appointments.vue'

import Treatments from './components/Treatments/Treatments.vue'
import NewTreatment from './components/Treatments/NewTreatment.vue'

import Billings from './components/Billings.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  {path: '/user', name: 'AuthPage', component: AuthPage},
  {path: '/login', name: 'Login', component: Login},
  {path: '/register', name: 'Register', component: Register},
  { path: '/new-patient', component: NewPatient },
  { path: '/patients', component: Patients },
  { path: '/new-doctor', component: NewDoctor },
  { path: '/doctors', component: Doctors },
  { path: '/new-appointment', component: NewAppointment },
  { path: '/appointments', component: Appointments },
  { path: '/new-treatment', component: NewTreatment },
  { path: '/treatments', component: Treatments },
  { path: '/billings', component: Billings },

  {
    path: '/reports',
    component: () => import('./components/Reports/ReportLayout.vue'),
    children: [
      { path: '', name: 'ReportsDashboard', component: () => import('./components/Reports/ReportsDashboard.vue') },
      { path: 'doctors', name: 'DoctorReports', component: () => import('./components/Reports/DoctorReports.vue') },
      { path: 'patients', name: 'PatientReports', component: () => import('./components/Reports/PatientReports.vue') },
      { path: 'appointments', name: 'AppointmentReports', component: () => import('./components/Reports/AppointmentReports.vue') },
      { path: 'treatments', name: 'TreatmentReports', component: () => import('./components/Reports/TreatmentReports.vue') },
      { path: 'billings', name: 'BillingReports', component: () => import('./components/Reports/BillingReports.vue') }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
