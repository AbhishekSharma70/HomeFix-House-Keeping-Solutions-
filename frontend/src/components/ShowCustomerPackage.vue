<template>
  <nav class="navbar navbar-expand-lg mb-4 shadow-sm bg-primary text-white">
    <div class="container-fluid">
      <a class="navbar-brand text-white" @click="goToCustomerDashboard">HomeFix | Service Packages</a>
    </div>
    <div class="d-flex justify-content-between mb-4">
      <button @click="logout" class="btn btn-danger mx-1">Logout</button>
    </div>
  </nav>

  <div class="container mt-5">
    <div class="professional-packages">
    <h2 class="text-center mb-4">Select Service Type {{ serviceName }}</h2>
    <form @submit.prevent="searchPackages" class="mb-4">
      <div class="mb-3">
        <label for="serviceType" class="form-label">Service Type</label>
        <select id="serviceType" v-model="serviceType" class="form-select" required>
          <option value="Carpenter">Carpenter</option>
          <option value="Plumber">Plumber</option>
          <option value="AC Repair">AC Repair</option>
          <option value="Saloon">Saloon</option>
          <option value="Cleaner">Cleaner</option>
          <option value="Painter">Painter</option>
        </select>
      </div>
      <button type="submit" class="btn btn-primary">Search Packages</button>
    </form>
  

    <div v-if="servicePackages.length > 0" class="mt-4">
      <h3>Available Packages</h3>
      <ul class="list-group mt-4">
        <li v-for="pkg in servicePackages" :key="pkg.id" class="list-group-item p-4 mb-3 shadow-sm">
          <h5 class="mb-2">{{ pkg.name }} 
            <span class="text-muted">({{ pkg.professional_name }} - Pincode: {{ pkg.professional_pincode }})</span>
          </h5>
          <p class="mb-1"><strong>Price:</strong> ₹{{ pkg.price }}</p>
          <p class="mb-1"><strong>Time Required:</strong> {{ pkg.time_required }}</p>
          <p><strong>Description:</strong> {{ pkg.description }}</p>

          <button @click="bookPackage(pkg.id)" class="btn btn-success mt-3">Book</button>
        </li>
      </ul>
    </div>
    
    <div v-else class="mt-4 text-center">
      <p class="text-muted">No packages found for the selected service type.</p>
    </div>
  </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      serviceType: '',
      servicePackages: []
    };
  },
  methods: {
    
    async searchPackages() {
      try {
        const token=localStorage.getItem('jwtToken')
        if(!token){
          alert('You are not logged in,Redirecting you to the login page')
          this.$router.push('CustomerLogin')
          return;
        }
        const customerId = localStorage.getItem('customerId');
        const response = await fetch(`http://localhost:8000/api/service_packages?service_type=${this.serviceType}&customer_id=${customerId}`,{
          'headers':{
            'Content-Type':'application/json',
            'Authorization':`Bearer ${token}`
          }
        });
        
        if (response.ok) {
          const data = await response.json();
          this.servicePackages = data.service_packages;
        } else {
          const errorData = await response.json();
          alert(errorData.message || 'Failed to fetch service packages');
        }
      } catch (error) {
        console.error('Error fetching service packages:', error);
        alert('An error occurred. Please try again.');
      }
    },

    async bookPackage(packageId) {
      try {
        const token=localStorage.getItem('jwtToken')
        if(!token){
          alert('You are not logged in,Redirecting you to the login page')
          this.$router.push({'name':'CustomerLogin'})
          return;
        }
        const customerId = localStorage.getItem('customerId');
        const response = await fetch(`http://localhost:8000/api/book_service/${packageId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization':`Bearer ${token}`
          },
          body: JSON.stringify({ customer_id: customerId })
        });
        
        const data = await response.json();
        if (response.ok) {
          alert('Package booked successfully!');
        } else {
          alert(data.error || 'Failed to book the package');
        }
      } catch (error) {
        console.error('Error booking package:', error);
        alert('An error occurred. Please try again.');
      }
    },

    goToCustomerDashboard(){
      this.$router.push({ name: 'CustomerDashboard' });
    },

    logout() {
      localStorage.removeItem('customerId');
      localStorage.removeItem('jwtToken')
      this.$router.push({ name: 'IndexFirst' });
    }
  }
};
</script>

<style>

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

.professional-packages {
  padding: 30px;
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.container {
  max-width: 800px;
}

.list-group-item {
  border-radius: 10px;
  background-color: #f9f9f9;
}

.text-center {
  color: #6c757d;
}

.btn {
  padding: 10px 20px;
}

h3 {
  font-weight: bold;
}
</style>