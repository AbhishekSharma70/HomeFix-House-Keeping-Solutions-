<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary mb-0">
    <div class="container-fluid">
      <a class="navbar-brand text-white" @click="goToProfessionalDashboard"> HomeFix | Service Request</a>
    </div>
  </nav>

  
    <div class="container d-flex justify-content-center mt-5">
      <div class="card shadow-lg p-4 w-40" style="background-color: #f7fafc">
        <h2 class="text-center mb-4">Create Service Package</h2>

         <form @submit.prevent="createServicePackage">
           <div class="mb-3">
            <label for="name" class="form-label">Package Name</label>
            <input type="text" id="name" v-model="name" class="form-control" required />
           </div>

           <div class="mb-3">
            <label for="price" class="form-label">Price</label>
            <input type="number" id="price" v-model="price" class="form-control" required />
           </div>

           <div class="form-floating mb-3">
            <select v-model="selectedServiceType" @change="fetchProfessionals" class="form-select" id="service_type" required>
              <option value="" disabled>Select a Service Type</option>
              <option v-for="type in serviceTypes" :key="type" :value="type">{{ type }}</option>
            </select>
            <label for="service_type">Service Type</label>
          </div>

           <div class="mb-3">
            <label for="timeRequired" class="form-label">Time Required (in hours)</label>
            <input type="text" id="timeRequired" v-model="timeRequired" class="form-control" required />
           </div>

           <div class="mb-3">
            <label for="description" class="form-label">Description</label>
            <textarea id="description" v-model="description" class="form-control" rows="3" required></textarea>
           </div>

           <button type="submit" class="btn btn-primary btn-block">Create Package</button>
        </form>
      </div>
    </div>

</template>

<script>
export default {
  data() {
    return {
      name: '',
      price: '',
      timeRequired: '',
      description: '',
      selectedServiceType : '',
      serviceTypes: ['Carpenter', 'Plumber', 'AC Repair', 'Cleaner', 'Painter', 'Saloon'],
    }; 
  },
  methods: {
    async createServicePackage() {
      try {
         const token=localStorage.getItem('jwtToken')
         if(!token){
          alert('You are not logged in,Redirecting you to Login Page.')
          this.$router.push({'name':'ServiceProfessionalLogin'})
          return;
         }
         const professionalId = localStorage.getItem('professionalId');
         const response = await fetch('http://localhost:8000/api/services', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json',
            'Authorization':`Bearer ${token}`
           },
          body: JSON.stringify({
            professional_id: professionalId,
            name: this.name,
            price: this.price,
            service_type: this.selectedServiceType,
            time_required: this.timeRequired,
            description: this.description
          }),
        });
        if (response.ok) {
          alert('Package created successfully!');
          this.resetForm();
        } else {
          alert('Failed to create package');
        }
      } catch (error) {
        console.error('Error creating package:', error);
      }
    },
    resetForm() {
      this.name = '';
      this.price = '';
      this.serviceType = '';
      this.timeRequired = '';
      this.description = '';
    },
    goToProfessionalDashboard(){
      this.$router.push({'name':'ServiceProfessionalDashboard'})
    }
  }
};
</script>

<style>
.card {
  border-radius: 10px;
}

.btn {
  border-radius: 5px;
}
</style>