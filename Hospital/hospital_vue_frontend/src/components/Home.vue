<template>
  <div>
    <!-- Hero Section -->
    <section class="container-fluid bg-light py-5">
      <div class="row align-items-center">
        <div class="col-md-6 text-center text-md-start px-4">
          <h2 class="display-6 fw-bold mb-3">Your Partner In Health and Wellness</h2>
          <p class="text-muted mb-4">
            Streamline hospital operations and enhance patient care with our smart Hospital Management System.
          </p>
          <router-link to="/new-appointment">
            <button class="btn btn-primary">Book An Appointment</button>
          </router-link>
        </div>
        <div class="col-md-6 text-center">
          <img
            src="/hospital-hero.jpg"
            alt="Doctor"
            class="img-fluid"
            style="max-width: 300px; height: 300px;"
          />
        </div>
      </div>
    </section>

    <!-- About Section -->
    <section class="container py-5">
      <h3 class="text-center fw-bold mb-4">About Our Hospital Management System</h3>
      <p class="text-center text-muted mb-4">
        Our system is designed to manage hospital activities such as patient admissions, doctor appointments, treatment records, billing, and much more. It provides a centralized platform for managing hospital data efficiently and securely.
      </p>
      <div class="row text-center">
        <div class="col-md-4">
          <i class="fas fa-database fa-3x text-primary mb-3"></i>
          <h5>Centralized Data</h5>
          <p class="small">All patient, doctor, and treatment records stored in one place.</p>
        </div>
        <div class="col-md-4">
          <i class="fas fa-clock fa-3x text-primary mb-3"></i>
          <h5>Real-time Scheduling</h5>
          <p class="small">Manage doctor availability and book appointments in real-time.</p>
        </div>
        <div class="col-md-4">
          <i class="fas fa-shield-alt fa-3x text-primary mb-3"></i>
          <h5>Secure Access</h5>
          <p class="small">Access control ensures data privacy and user-specific roles.</p>
        </div>
      </div>
    </section>

    <!-- Why Choose Us -->
    <section class="bg-primary text-white text-center py-5">
      <h3 class="fw-bold mb-4">Why Choose Our Solution?</h3>
      <div class="row justify-content-center">
        <div class="col-md-3 mb-4">
          <i class="fas fa-check-circle fa-2x mb-2"></i>
          <h6>Easy To Use</h6>
          <p class="small">User-friendly interface for staff and administrators.</p>
        </div>
        <div class="col-md-3 mb-4">
          <i class="fas fa-mobile-alt fa-2x mb-2"></i>
          <h6>Responsive Design</h6>
          <p class="small">Access on desktop, tablet, or mobile seamlessly.</p>
        </div>
        <div class="col-md-3 mb-4">
          <i class="fas fa-chart-line fa-2x mb-2"></i>
          <h6>Reports & Analytics</h6>
          <p class="small">Track trends in treatments, appointments, and billing.</p>
        </div>
      </div>
    </section>

    <!-- Testimonials Section -->
    <section class="container text-center py-5">
      <h3 class="mb-4 fw-bold">What Users Say</h3>
      <div class="row">
        <div class="col-md-4">
          <blockquote class="blockquote">
            <p class="mb-3">"The best hospital management system we’ve used. Organized and efficient!"</p>
            <footer class="blockquote-footer">Dr. Smith, Cardiology</footer>
          </blockquote>
        </div>
        <div class="col-md-4">
          <blockquote class="blockquote">
            <p class="mb-3">"Easy to manage appointments and treatments. Highly recommend."</p>
            <footer class="blockquote-footer">Nurse Amelia, Pediatrics</footer>
          </blockquote>
        </div>
        <div class="col-md-4">
          <blockquote class="blockquote">
            <p class="mb-3">"We’ve saved time and improved patient care since using it."</p>
            <footer class="blockquote-footer">Admin John, Front Desk</footer>
          </blockquote>
        </div>
      </div>
    </section>

    <!-- Call To Action -->
    <section class="bg-light py-5 text-center">
      <h4 class="fw-bold mb-3">Ready to Modernize Your Hospital?</h4>
      <p class="mb-4 text-muted">Try our system now or contact us to schedule a demo.</p>
      <router-link to="/doctors">
        <button class="btn btn-outline-primary">Find Doctor</button>
      </router-link>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomePage'
}
</script>

<style scoped>
/* Add any extra home page-specific styles here */
</style>
