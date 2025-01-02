<template>
  <nav class="navbar navbar-expand-lg mb-4 shadow-sm bg-primary text-white">
    <div class="container-fluid">
      <a class="navbar-brand text-white" @click="goToAdminDashboard">HomeFix | Manage HomeFix Packages</a>
    </div>
  </nav>
  <div class="container mt-5">
    <h1 class="text-center mb-5 fw-bold">Manage HomeFix Packages</h1>

    <!-- Dropdown to select service type -->
    <div class="form-group mb-4">
      <label for="serviceType" class="form-label fs-5">Select Service Type</label>
      <select v-model="selectedServiceType" class="form-select form-select-lg shadow-sm">
        <option value="" disabled>Select a service type</option>
        <option value="Plumber">Plumber</option>
        <option value="Carpenter">Carpenter</option>
        <option value="AC Repair">AC Repair</option>
        <option value="Saloon">Saloon</option>
        <option value="Cleaner">Cleaner</option>
        <option value="Painter">Painter</option>
      </select>
    </div>

    <!-- Search button to fetch packages -->
    <button @click="fetchPackages" class="btn btn-primary btn-lg w-100 shadow-sm">Search Packages</button>

    <!-- Display packages once fetched -->
    <div v-if="adminPackages.length > 0" class="d-flex flex-column align-items-center mt-5">
      <div v-for="pkg in adminPackages" :key="pkg.id" class="card mb-4 package-card shadow-sm">
        <div class="card-body text-center">
          <h5 class="card-title fw-bold text-primary">{{ pkg.package_name }}</h5>
          <p class="card-text">
            <strong>Description:</strong> {{ pkg.description }} <br>
            <strong>Time Required:</strong> {{ pkg.time_required }} <br>
            <strong>Service Professional:</strong> {{ pkg.professional_name }}
          </p>
          <div class="d-flex justify-content-around mt-4">
            <button @click="updatePackage(pkg)" class="btn btn-outline-warning btn-sm shadow-sm">
              Update
            </button>
            <button @click="deletePackage(pkg.id)" class="btn btn-outline-danger btn-sm shadow-sm">
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedServiceType: '',
      adminPackages: []
    };
  },
  methods: {
    async fetchPackages() {
      const token=localStorage.getItem('jwtToken')
      if(!token){
        alert('You are not logged in,Redirecting you to the login page')
        this.$router.push({'name':'AdminLogin'})
        return;
      }
      // Fetch admin service packages by selected service type
      try {
        const response = await fetch(`http://localhost:8000/api/admin_service_packages/${this.selectedServiceType}`,{
          headers:{
            'Content-Type':'application/json',
            'Authorization':`Bearer ${token}`
          }
        });
        const data = await response.json();
        this.adminPackages = data.packages || [];
      } catch (error) {
        console.error('Error fetching packages:', error);
      }
    },
    updatePackage(pkg) {
      this.$router.push({ name: 'HomeFixUpdatePackage', params: { pkgId: pkg.id } });
    },
    async deletePackage(pkgId) {
      const token=localStorage.getItem('jwtToken')
      if(!token){
        alert('You are not logged in,Redirecting you to the login page')
        this.$router.push({'name':'AdminLogin'})
        return;
      }
      // Call API to delete the package
      try {
        const response = await fetch(`http://localhost:8000/api/delete_service_package/${pkgId}`, {
          method: 'DELETE',
          headers:{
            'Content-Type':'application/json',
            'Authorization':`Bearer ${token}`
          }
        });
        const data=await response.json()
        if (response.ok) {
           alert(data.message);
           this.fetchPackages();
        } else {
          alert('Failed to delete package');
        }
      } catch (error) {
        console.error('Error deleting package:', error);
      }
    },
    goToAdminDashboard(){
      this.$router.push({ name: 'AdminDashboard' });
    }
  }
};
</script>

<style scoped>
/* Global Container Styling */
.container {
  max-width: 750px;
}

/* Navbar Styling */
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

/* Form Select Styling */
.form-select {
  padding: 1rem;
  font-size: 1rem;
  border-radius: 0.5rem;
  border: 1px solid #ced4da;
  background-color: #f9f9f9;
}

.form-select:focus {
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

/* Button Styling */
button {
  font-weight: 500;
  transition: transform 0.2s ease;
}

button:hover {
  transform: translateY(-1px);
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
}

/* Package Card Styling */
.package-card {
  width: 90%;
  max-width: 600px;
  border-radius: 10px;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
  transition: transform 0.3s ease;
}

.package-card:hover {
  transform: scale(1.02);
}

.card-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #007bff;
}

.card-text {
  font-size: 1rem;
  line-height: 1.5;
  color: #333;
}

/* Action Button Styling */
.btn-outline-warning, .btn-outline-danger {
  width: 45%;
  font-size: 0.85rem;
}

.btn-outline-warning:hover {
  background-color: #ffc107;
  color: white;
}

.btn-outline-danger:hover {
  background-color: #dc3545;
  color: white;
}
</style>