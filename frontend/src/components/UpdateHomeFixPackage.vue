<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary mb-0">
    <div class="container-fluid">
      <a class="navbar-brand text-white" @click="goToAdminDashboard">HomeFix | Update HomeFix Package</a>
    </div>
  </nav>
  <br>
  <div class="update-service-package">
    <h2 class="form-title">Update HomeFix Package</h2>
    <div class="container-fluid d-flex justify-content-center align-items-center" style="margin-top: 50px;" id="app">
     <div class="card p-4 form-card shadow-lg">
      <div class="card-body text-center">
          <form @submit.prevent="updateService">
            <div class="form-group">
              <label for="name" class="form-label">Service Name:</label>
              <input type="text" v-model="form.package_name" required class="form-control" />
            </div>

            <br>

            <div class="form-group">
              <label for="base_price " class="form-label">Base Price:</label>
              <input type="number" v-model="form.base_price" required class="form-control" />
            </div>

            <br>

            <div class="form-group">
              <label for="time_required" class="form-label">Time Required (in hours):</label>
              <input type="text" v-model="form.time_required" required class="form-control" />
            </div>

            <br>

            <div class="form-group">
              <label for="description" class="form-label">Description:</label>
              <textarea v-model="form.description" class="form-control"></textarea>
            </div>

            <br>

            <div class="form-group">
              <label for="service_type" class="form-label">Service Type:</label>
              <select v-model="selectedServiceType" @change="fetchProfessionals" required class="form-control">
                <option value="">Select a Service Type</option>
                <option v-for="type in serviceTypes" :key="type" :value="type">{{ type }}</option>
              </select>
            </div>

            <br>

            <div class="form-group" v-if="professionals.length">
              <label for="service_professional" class="form-label">Select Service Professional:</label>
              <select v-model="form.service_professional_id" required class="form-control">
                <option value="">Select a Professional</option>
                <option v-for="professional in professionals" :key="professional.id" :value="professional.id">
                  {{ professional.full_name }}
                </option>
              </select>
              <!-- Show the view profile link next to the dropdown -->
              <div v-if="form.service_professional_id">
                <router-link 
                  :to="{ name: 'ProfessionalProfileAdmin', params: { id: form.service_professional_id } }" 
                  class="view-profile-link" 
                  target="_blank">
                  View Profile
                </router-link>
              </div>
            </div>

            <br>
            <button type="submit" class="btn btn-primary">Update Service Package</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        package_name: '',
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
  created() {
    this.fetchPackageDetails();
  },
  methods: {
    fetchPackageDetails() {
      const token=localStorage.getItem('jwtToken')
      if(!token){
        alert('You are not logged in,Redirecting you to the login page')
        this.$router.push({'name':'AdminLogin'})
        return;
      }
      const pkgId = this.$route.params.pkgId;
      fetch(`http://localhost:8000/api/service_package/${pkgId}`,{
        headers:{
          'Content-Type':'application/json',
          'Authorization':`Bearer ${token}`
        }
      })
        .then((response) => response.json())
        .then((data) => {
          this.form = data.package;
          this.selectedServiceType = data.package.service_type;
          this.fetchProfessionals();
        })
        .catch((error) => console.error('Error fetching package details:', error));
    },
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
          .catch((error) => console.error('Error fetching professionals:', error));
      }
    },
    updateService() {
      const token=localStorage.getItem('jwtToken')
      if(!token){
        alert('You are not logged in,Redirecting you to the login page')
        this.$router.push({'name':'AdminLogin'})
        return;
      }
      const pkgId = this.$route.params.pkgId;
      const serviceData = {
        package_name: this.form.package_name,
        base_price: this.form.base_price,
        time_required: this.form.time_required,
        description: this.form.description,
        service_type: this.selectedServiceType,
        service_professional_id: this.form.service_professional_id,
      };

      fetch(`http://localhost:8000/api/update_service_package/${pkgId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization':`Bearer ${token}`
        },
        body: JSON.stringify(serviceData),
      })
        .then((response) => response.json())
        .then((data) => {
          alert(data.message || 'Service package updated successfully!');
          this.$router.push({ name: 'AdminDashboard' });
        })
        .catch((error) => console.error('Error updating service package:', error));
    },
    goToAdminDashboard() {
      this.$router.push({ name: 'AdminDashboard' });
    },
  },
};
</script>

<style>
.update-service-package {
  padding: 2rem;
}
.form-control {
  max-width: 500px;
}
.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}
.btn-primary:hover {
  background-color: #0056b3;
  border-color: #0056b3;
}
.view-profile-link {
  margin-left: 10px;
  color: blue;
  text-decoration: underline;
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

.form-card {
  background-color: #e0f7fa;
  max-width: 400px;
  width: 100%;
  border-radius: 12px;
}

.form-title {
  color: #00796b;
  font-weight: 700;
}

.activity-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  position: relative;
}

.form-label {
  font-weight: 500;
  color: #00796b;
  font-size: 14px;
}

.form-control {
  border: none;
  border-bottom: 2px solid #00796b;
  border-radius: 0;
  box-shadow: none;
  padding: 10px;
  transition: border-color 0.3s;
}

.form-control:focus {
  border-color: #004d40;
  box-shadow: none;
}

.form-submit-btn {
  background-color: #00796b;
  border: none;
  color: white;
  padding: 10px;
  border-radius: 6px;
  font-weight: 600;
  transition: background-color 0.3s;
}

.form-submit-btn:hover {
  background-color: #004d40;
  color: white;
}

</style>