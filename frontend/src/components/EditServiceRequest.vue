<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary mb-0">
    <div class="container-fluid">
        <a class="navbar-brand" @click="goToCustomerDashboard">HomeFix | Requested Services</a>
    </div>
    <div class="d-flex justify-content-between mb-4">
        <button @click="logout" class="btn btn-danger mx-1">Logout</button>
    </div>
</nav>
<div class="container mt-5">
    <div style="background-color:#e0f7fa" class="card shadow-sm p-4">
      <h2 class="text-center mb-4">Edit Service Request</h2>
      <form @submit.prevent="updateServiceRequest">
        <div class="mb-3">
          <label for="date_of_request" class="form-label">Date of Request:</label>
          <input type="date" v-model="date_of_request" class="form-control" required />
        </div>

        <div class="mb-3">
          <label for="description" class="form-label">Description:</label>
          <textarea v-model="description" class="form-control" rows="4" required></textarea>
        </div>

        <div class="mb-3">
          <label for="price" class="form-label">Price:</label>
          <input type="number" v-model="price" class="form-control" required />
        </div>

        <button type="submit" class="btn btn-primary w-100">Update Request</button>
      </form>
    </div>
  </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        date_of_request: '',
        description: '',
        price: 0,
        serviceRequestId: this.$route.params.requestId, // Assuming you pass the request ID as a route parameter
      };
    },
    methods: {
      async updateServiceRequest() {
        const response = await fetch(`http://localhost:8000/api/service_requests/${this.serviceRequestId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            date_of_request: this.date_of_request,
            description: this.description,
            price: this.price,
          }),
        });
  
        if (response.ok) {
          alert('Service request updated successfully.');
          this.$router.push('/customer-dashboard'); // Redirect to customer dashboard
        } else {
          const data = await response.json();
          alert(data.error || 'Failed to update the request.');
        }
      },
      goToCustomerDashboard(){
        this.$router.push({name:'RequestedService'})
      },
      logout(){
      localStorage.removeItem('customerId');
      this.$router.push({ name: 'IndexFirst' });
     },
    },
  };
  </script>
  
  <style scoped>
  .card {
    max-width: 500px;
    margin: 0 auto;
  }
</style>