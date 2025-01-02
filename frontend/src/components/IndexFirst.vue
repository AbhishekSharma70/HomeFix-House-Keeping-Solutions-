<template>
  <div class="d-flex flex-column min-vh-100">
    <nav class="navbar navbar-expand-lg mb-4 shadow-sm bg-primary text-white">
      <div class="container-fluid">
        <a class="navbar-brand text-white" href="#">HomeFix</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo02" aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarTogglerDemo02">
          <div class="ms-auto d-flex">
            <!-- Signup Dropdown -->
            <div class="dropdown me-3">
              <button class="btn btn-info dropdown-toggle" type="button" id="signupDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                Sign Up
              </button>
              <ul class="dropdown-menu" aria-labelledby="signupDropdown">
                <li><button class="dropdown-item" @click="navigateTo('/admin_signup')">Admin</button></li>
                <li><button class="dropdown-item" @click="navigateTo('/customer_signup')">Customer</button></li>
                <li><button class="dropdown-item" @click="navigateTo('/serviceprofessional_signup')">Service Professional</button></li>
              </ul>
            </div>

            <!-- Login Dropdown -->
            <div class="dropdown">
              <button class="btn btn-success dropdown-toggle margin-left" type="button" id="loginDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                Login
              </button>
              <ul class="dropdown-menu" aria-labelledby="loginDropdown">
                <li><button class="dropdown-item" @click="navigateTo('/admin_login')">Admin</button></li>
                <li><button class="dropdown-item" @click="navigateTo('/customer_login')">Customer</button></li>
                <li><button class="dropdown-item" @click="navigateTo('/serviceprofessional_login')">Service Professional</button></li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <main class="flex-fill">
      <div class="container text-center" style="margin-top:60px;">
        <h2 class="fw-bold">Who Are We?</h2>
        <p class="lead">HomeFix connects homeowners with a wide range of trusted service professionals such as plumbers, electricians, cleaners, painters, carpenters, and more, to address various household needs.</p>
      </div>

      <div class="container mt-4">
        <div class="row row-cols-1 row-cols-md-3 g-4 justify-content-center">
          <div class="col">
            <div class="card h-100 shadow-sm">
              <img src="/images/carpenter1.jpg" class="card-img-top" style="height: 200px; object-fit: cover;" alt="Carpenter">
              <div class="card-body">
                <h5 class="card-title">Carpenter Services</h5>
                <p class="card-text">Skilled local carpenters for quick repairs and custom work. Reliable, efficient, and ready to help nearby.</p>
              </div>
            </div>
          </div>

          <div class="col">
            <div class="card h-100 shadow-sm">
              <img src="/images/plumber1.webp" class="card-img-top" style="height: 200px; object-fit: cover;" alt="Plumber">
              <div class="card-body">
                <h5 class="card-title">Plumbing Services</h5>
                <p class="card-text">Expert local plumbers for fast fixes and urgent repairs. Nearby and available for immediate, reliable service.</p>
              </div>
            </div>
          </div>

          <div class="col">
            <div class="card h-100 shadow-sm">
              <img src="/images/painter1.jpg" class="card-img-top" style="height: 200px; object-fit: cover;" alt="Painter">
              <div class="card-body">
                <h5 class="card-title">Painter Services</h5>
                <p class="card-text">Professional painters close by for timely, high-quality painting. Local experts providing fast, detailed service.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <footer class="py-3 my-4 bg-light">
      <div class="container">
        <ul class="nav justify-content-center border-bottom pb-3 mb-3">
          <li class="nav-item"><button @click="navigateTo('/')" class="nav-link px-2 text-muted">Home</button></li>
          <li class="nav-item"><button @click="navigateTo('/about')" class="nav-link px-2 text-muted">About</button></li>
        </ul>
        <p class="text-center text-muted">© 2024 HomeFix, PVT.LTD</p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  methods: {
    navigateTo(route) {
      this.$router.push(route);
    }
  }
}
</script>

<style scoped>


body {
  font-family: 'Helvetica Neue', Arial, sans-serif;
  text-align: center;
}

.navbar {
  background: linear-gradient(90deg, #8ad3e3 0%, #2a5298 100%);
  color: white;
  font-weight: bold;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.navbar-brand {
  font-weight: bold;
  font-size: 1.3rem;
  cursor: pointer;
}

.card {
  transition: transform 0.2s;
}

.card:hover {
  transform: scale(1.05);
}

h2 {
  margin-bottom: 20px;
}

p.lead {
  margin: 20px auto;
  max-width: 800px;
}

footer {
  background-color: #f8f9fa;
}

.margin-left{
    margin-right: 40px !important;
}

/* Add this CSS to align buttons inline */
.dropdown {
  display: inline-block;
  margin-right: 10px; /* Adjust spacing between dropdowns */
}
</style>