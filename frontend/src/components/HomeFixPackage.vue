<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light mb-3">
    <div class="container-fluid">
      <a class="navbar-brand text-white" @click="goToCustomerDashboard">HomeFix | HomeFix Packages</a>
      <div class="d-flex">
        <button @click="logout" class="btn btn-danger">Logout</button>
      </div>
    </div>
  </nav>
  <br>
  <br>

  <div class="container">
    <div class="homefix-packages">
      <h2 class="text-center mb-4">Select a Service Type</h2>
      <div class="form-group mb-4">
        <label for="service_type" class="form-label">Service Type:</label>
        <select v-model="selectedServiceType" class="form-select">
          <option value="">Select</option>
          <option v-for="type in serviceTypes" :key="type" :value="type">{{ type }}</option>
        </select>
        <button @click="searchPackages" class="btn btn-primary mt-3">Search Packages</button>
      </div>

      <div v-if="packages.length" class="packages-list">
        <h3 class="text-center mb-4">Available Packages</h3>
        <div class="row">
          <div class="col-md-6 col-lg-4 mb-4" v-for="pkg in packages" :key="pkg.id">
            <div class="card h-100 shadow-sm ">
              <div class="card-body">
                <h4 class="card-title">{{ pkg.name }} ({{ pkg.service_type }})</h4>
                <p class="card-text">{{ pkg.description }}</p>
                <p class="card-text"><strong>Price:</strong> ₹{{ pkg.base_price }}</p>
                <p class="card-text"><strong>Professional ID:</strong> {{ pkg.service_professional_id }}</p>
              </div>
              <div class="card-footer text-center">
                <button @click="bookPackage(pkg.id, pkg.service_professional_id)" class="btn btn-success">Book Package</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="searched" class="mt-4 text-center">
        <p class="alert alert-warning">No packages available for the selected service type.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedServiceType: '',
      serviceTypes: ['Carpenter', 'Plumber', 'AC Repair', 'Cleaner', 'Painter', 'Saloon'],
      packages: [],
      searched: false,
    };
  },
  methods: {
    searchPackages() {
      const token=localStorage.getItem('jwtToken')
      if(!token){
        alert('You are not logged in,Redirecting you to the login page')
        this.$router.push({'name':'CustomerLogin'})
        return
      }
      if (this.selectedServiceType) {
        fetch(`http://localhost:8000/api/packages/${this.selectedServiceType}`,{
          'headers':{
            'Content-Type':'application/json',
            'Authorization':`Bearer ${token}`
          }
        })
          .then((response) => response.json())
          .then((data) => {
            this.packages = data;
            this.searched = true;
          })
          .catch((error) => {
            console.error('Error fetching packages:', error);
          });
      } else {
        alert('Please select a service type');
      }
    },
    bookPackage(packageId, serviceProfessionalId) {
      const customerId = localStorage.getItem('customerId');
      const currentDate = new Date().toISOString().slice(0, 10);
      const bookingData = {
        customer_id: customerId,
        package_id: packageId,
        service_professional_id: serviceProfessionalId,
        date_of_request: currentDate,
      };
      const token=localStorage.getItem('jwtToken')
      if(!token){
        alert('You are not logged in,Redirecting you to the login page')
        this.$router.push({'name':'CustomerLogin'})
        return;
      }
      fetch('http://localhost:8000/api/book_package', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization':`Bearer ${token}`
        },
        body: JSON.stringify(bookingData),
      })
        .then((response) => response.json())
        .then((data) => {
          alert(data.message || 'Package booked successfully!');
        })
        .catch((error) => {
          console.error('Error booking package:', error);
        });
    },
    goToCustomerDashboard() {
      this.$router.push({ name: 'CustomerDashboard' });
    },
    logout() {
      localStorage.removeItem('customerId');
      this.$router.push({ name: 'IndexFirst' });
    }
  },
};
</script>

<style scoped>
.homefix-packages {
  padding: 30px;
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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
  transition: transform 0.2s ease;
}

.card:hover {
  transform: translateY(-5px);
}

.card-title {
  font-weight: 700;
}

.card-footer {
  background-color: #ffffff;
  border-top: none;
}
</style>