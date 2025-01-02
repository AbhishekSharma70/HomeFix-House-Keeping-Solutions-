<template>
  <!-- Navbar -->
  <nav class="navbar navbar-expand-lg mb-4 shadow">
    <div class="container-fluid">
      <a class="navbar-brand text-white" @click="goToAdminDashboard">HomeFix | Create HomeFix Package</a>
    </div>
  </nav>

  <!-- Form Container -->
  <div class="container mt-5 align-center">
    <div class="card form-card shadow-lg">
      <div class="card-header text-white text-center">
        <h2 class="h4 mb-0">Create Service Package</h2>
      </div>
      <div class="card-body">
        <form @submit.prevent="createService">
          <div class="form-floating mb-3">
            <input type="text" v-model="form.name" class="form-control" id="name" placeholder="Service Name" required />
            <label for="name">Service Name</label>
          </div>

          <div class="form-floating mb-3">
            <input type="number" v-model="form.base_price" class="form-control" id="base_price" placeholder="Base Price" required />
            <label for="base_price">Base Price</label>
          </div>

          <div class="form-floating mb-3">
            <input type="text" v-model="form.time_required" class="form-control" id="time_required" placeholder="Time Required" required />
            <label for="time_required">Time Required (in hours)</label>
          </div>

          <div class="form-floating mb-3">
            <textarea v-model="form.description" class="form-control" id="description" placeholder="Description" style="height: 100px"></textarea>
            <label for="description">Description</label>
          </div>

          <div class="form-floating mb-3">
            <select v-model="selectedServiceType" @change="fetchProfessionals" class="form-select" id="service_type" required>
              <option value="" disabled>Select a Service Type</option>
              <option v-for="type in serviceTypes" :key="type" :value="type">{{ type }}</option>
            </select>
            <label for="service_type">Service Type</label>
          </div>

          <div v-if="professionals.length" class="form-floating mb-3">
            <select v-model="form.service_professional_id" class="form-select" id="service_professional" required>
              <option value="" disabled>Select a Professional</option>
              <option v-for="professional in professionals" :key="professional.id" :value="professional.id">
                {{ professional.full_name }}
              </option>
            </select>
            <label for="service_professional">Service Professional</label>
            <div v-if="form.service_professional_id" class="mt-2 text-middle">
              <router-link :to="{ name: 'ProfessionalProfileAdmin', params: { id: form.service_professional_id } }" class="view-profile-link" target="_blank">
                View Profile
              </router-link>
            </div>
          </div>

          <div class="d-grid mt-4">
            <button type="submit" class="btn btn-primary btn-lg">Create Service Package</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        name: '',
        base_price: 0,
        time_required: '',
        description: '',
        service_professional_id: null,
      },
      selectedServiceType: '',
      serviceTypes: ['Carpenter', 'Plumber', 'AC Repair', 'Cleaner', 'Painter', 'Saloon'],
      professionals: [],
    };
  },
  methods: {
    fetchProfessionals() {
      const token=localStorage.getItem('jwtToken')
      if(!token){
        alert('You are not logged in,Redirecting you to the login page')
        this.$router.push({'name':'AdminLogin'})
        return;
      }
      if (this.selectedServiceType) {
        fetch(`http://localhost:8000/api/service-professionals/${this.selectedServiceType}`,{
          headers:{
            'Content-Type':'application/json',
            'Authorization':`Bearer ${token}`
          }
        })
          .then((response) => response.json())
          .then((data) => {
            this.professionals = data;
          })
          .catch((error) => {
            console.error('Error fetching professionals:', error);
          });
      }
    },
    createService() {
      const token=localStorage.getItem('jwtToken')
      if(!token){
        alert('You are not logged in,Redirecting you to the login page')
        this.$router.push({'name':'AdminLogin'})
        return;
      }
      const serviceData = {
        name: this.form.name,
        base_price: this.form.base_price,
        time_required: this.form.time_required,
        description: this.form.description,
        service_type: this.selectedServiceType,
        service_professional_id: this.form.service_professional_id,
      };

      fetch('http://localhost:8000/api/admin/services', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization':`Bearer ${token}`
        },
        body: JSON.stringify(serviceData),
      })
        .then((response) => response.json())
        .then((data) => {
          alert(data.message || 'Service created successfully!');
          this.resetForm();
        })
        .catch((error) => {
          console.error('Error creating service:', error);
        });
    },
    resetForm() {
      this.form = {
        name: '',
        base_price: 0,
        time_required: '',
        description: '',
        service_professional_id: null,
      };
      this.selectedServiceType = '';
      this.professionals = [];
    },
    goToAdminDashboard(){
      this.$router.push({ name: "AdminDashboard" });
    }
  },
};
</script>

<style scoped>
/* Navbar Styling */
.navbar {
  background: linear-gradient(90deg, #8ad3e3 0%, #2a5298 100%);
  color: white;
  font-weight: bold;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Centering Container */
.container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 80vh; /* Full height of the viewport */
}

/* Card and Form Styling */
.form-card {
  border-radius: 15px;
  overflow: hidden;
  background: linear-gradient(135deg, #e0f7fa 0%, #ffffff 100%);
  max-width: 500px; /* Adjust width as needed */
  width: 100%;
}

.card-header {
  background: #00796b;
  font-weight: 500;
}

.form-control,
.form-select {
  border-radius: 10px;
  background-color: #f1f5f9;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 1rem;
}

.form-control:focus,
.form-select:focus {
  box-shadow: 0 0 5px rgba(51, 102, 153, 0.4);
  border-color: #337ab7;
}

/* Profile Link */
.view-profile-link {
  font-size: 0.9rem;
  color: #007bff;
  text-decoration: underline;
}

button[type="submit"] {
  border-radius: 12px;
  font-weight: bold;
}
</style>