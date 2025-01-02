<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary mb-0">
    <div class="container-fluid">
      <a class="navbar-brand text-white" @click="goToCustomerDashboard"> HomeFix | Service Request</a>
    </div>
  </nav>


  <div class="container-fluid d-flex justify-content-center align-items-center" style="margin-top: 50px;" id="app">
    <div class="card p-4 form-card shadow-lg">
      <div class="card-body text-center">
        <div class="container mt-5 form-title">
          <h2 class="text-center mb-4">Request {{ serviceName }}</h2>
        </div>
        <form @submit.prevent="submitRequest">
          <!-- Date of Request -->
          <div class="mb-3 form-group">
            <label for="dateOfRequest" class="form-label">Date of Request</label>
            <input type="date" v-model="dateOfRequest" class="form-control" required />
          </div>

          <!-- Status of Service Request -->
          <div class="mb-3 form-group">
            <label for="serviceStatus" class="form-label">Status of Service Request</label>
            <select id="serviceStatus" v-model="serviceStatus" class="form-select" required>
              <option value="requested">Requested</option>
            </select>
          </div>

          <!-- Remarks -->
          <div class="mb-3 form-group">
            <label for="description" class="form-label">Description</label>
            <textarea id="description" v-model="description" class="form-control" rows="3"></textarea>
          </div>

          <!-- Price -->
          <div class="mb-3 form-group">
            <label for="price" class="form-label">Price (Rs.)</label>
            <input type="number" v-model="price" class="form-control" required min="0" placeholder="Enter a valid price">
          </div>

          <!-- Service Professional Selection -->
          <div class="mb-3 form-group">
            <label for="professional" class="form-label">Choose Service Professional</label>
            <select id="professional" v-model="professionalId" class="form-select" required>
              <option v-for="professional in availableProfessionals" :key="professional.id" :value="professional.id">
                {{ professional.fullname }}
              </option>
            </select>
            <div v-if="professionalId">
              <router-link :to="{ name: 'ProfessionalProfile', params: { professionalId: professionalId }}" @click="saveFormData">
                View Professional Profile
              </router-link>
            </div>
          </div>

          <!-- No Professionals Found -->
          <div v-if="!availableProfessionals.length" class="text-danger">No professionals available for this service.</div>

          <!-- Submit Button -->
          <button type="submit" class="btn btn-primary" :disabled="!availableProfessionals.length">Submit Request</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    serviceName: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      dateOfRequest: '',
      description: '',
      professionalId: null,
      availableProfessionals: [],
      serviceStatus: 'requested',
      price: ''
    };
  },
  created() {
    this.fetchAvailableProfessionals();
    this.loadFormData();
  },
  methods: {
    async fetchAvailableProfessionals() {
      try {
        const customerId=localStorage.getItem('customerId')
        const token=localStorage.getItem('jwtToken')
        const response = await fetch(`http://localhost:8000/api/professionals?service_type=${this.serviceName}`,{
          method:'GET',
          headers:{
            'Content-Type':'application/json',
            'Customer-ID':customerId,
            'Authorization':`Bearer ${token}`
          }
        });
        const data = await response.json();
        if (response.ok) {
          this.availableProfessionals = data.professionals;
        } else {
          console.error('Error fetching professionals:', data.message);
          this.availableProfessionals = [];
        }
      } catch (error) {
        console.error('Error fetching professionals:', error);
      }
    },
    saveFormData() {
      // Save form data to localStorage
      const formData = {
        dateOfRequest: this.dateOfRequest,
        description: this.description,
        professionalId: this.professionalId,
        serviceStatus: this.serviceStatus,
        price: this.price
      };
      localStorage.setItem('serviceRequestForm', JSON.stringify(formData));
    },
    loadFormData() {
      // Load form data from localStorage
      const savedData = localStorage.getItem('serviceRequestForm');
      if (savedData) {
        const formData = JSON.parse(savedData);
        this.dateOfRequest = formData.dateOfRequest;
        this.description = formData.description;
        this.professionalId = formData.professionalId;
        this.serviceStatus = formData.serviceStatus;
        this.price = formData.price;
      }
    },
    async submitRequest() {
      try {
        const customerId = localStorage.getItem('customerId');
        const response = await fetch('http://localhost:8000/api/service_requests', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            customer_id: customerId,
            professional_id: this.professionalId,
            description: this.description,
            date_of_request: this.dateOfRequest,
            service_status: this.serviceStatus,
            price: this.price
          })
        });
        const data = await response.json();
        if (response.ok) {
          alert('Service request submitted successfully!');
          this.resetForm();
        } else {
          alert(data.message || 'Failed to submit request');
        }
      } catch (error) {
        console.error('Error submitting request:', error);
        alert('An error occurred. Please try again.');
      }
    },
    resetForm() {
      this.dateOfRequest = '';
      this.description = '';
      this.professionalId = null;
      this.serviceStatus = 'requested';
      this.price = '';
      this.availableProfessionals = [];
      localStorage.removeItem('serviceRequestForm'); // Clear form data after successful submission
    },
    goToCustomerDashboard() {
      this.$router.push({ name: 'CustomerDashboard' });
    }
  }
};
</script>

<style scoped>

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