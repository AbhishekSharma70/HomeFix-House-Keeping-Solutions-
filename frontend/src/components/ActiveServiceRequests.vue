<template>

<nav class="navbar navbar-expand-lg bg-body-tertiary mb-0">
    <div class="container-fluid">
        <a class="navbar-brand text-white" @click="goToCustomerDashboard" >HomeFix | Service Requests </a>
    </div>
    <button @click="logout" class="btn btn-danger mx-1">Logout</button>
</nav>

<div class="container mt-5">
    <h2 class="text-center mb-4">Your Active Service Requests</h2>
    <table class="table table-striped">
      <thead>
        <tr>
          <th>Professional Id</th>
          <th>Professional Name</th>
          <th>Phone Number</th>
          <th>Service Type</th>
          <th>Description</th>
          <th>Status</th>
          <th>Date of Request</th>
          <th>Close</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="request in serviceRequests" :key="request.professional_id">
          <td>{{ request.professional_id }}</td>
          <td>{{ request.professional_name }}</td>
          <td>{{ request.phone_number }}</td>
          <td>{{ request.service_type }}</td>
          <td>{{ request.description }}</td>
          <td>{{ request.status }}</td>
          <td>{{ request.date_of_request }}</td>
          <td>
            <button 
              class="btn btn-success" 
              @click="navigateToCloseRequest(request.id)" 
              :disabled="request.status !== 'assigned'"
            >
              Close
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>


</template>

<script>
export default {
  data() {
    return {
      serviceRequests: [],
      remarks:'',
      rating:'',
    };
  },
  created(){
    this.fetchCustomerRequests();
  },
  methods: {
    logout(){
      localStorage.removeItem('customerId');
      localStorage.removeItem('jwtToken')
      this.$router.push({ name: 'IndexFirst' });
    },
    async fetchCustomerRequests() {
      const token=localStorage.getItem('jwtToken')
      if(!token){
        alert('You are not logged in, Redirecting to login page')
        this.$router.push({'name':'CustomerLogin'})
        return;
      }
      const customerId = localStorage.getItem('customerId');
      try {
        const response = await fetch(`http://localhost:8000/api/customer_requests/${customerId}`,{
          'headers':{
            'Content-Type':'Application/json',
            'Authorization':`Bearer ${token}`
          }
        });
        const data = await response.json();
        this.serviceRequests = data.service_requests;
      } catch (error) {
        console.error('Error fetching service requests:', error);
      }
    },
    navigateToCloseRequest(requestId){
      this.$router.push({name:'CloseServiceRequest',
      params:{requestId}})
    },
    goToCustomerDashboard(){
        this.$router.push({"name":"CustomerDashboard"})
    }
  }
};
</script>

<style scoped>
.service-image{
  width:100%;
  height:200px;
  object-fit:cover
}
</style>