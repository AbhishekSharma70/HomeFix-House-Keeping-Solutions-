<template>

<nav class="navbar navbar-expand-lg mb-4 shadow-sm bg-primary text-white">
    <div class="container-fluid">
      <a class="navbar-brand text-white" @click="goToCustomerDashboard">HomeFix | Service Requests</a>
    </div>
    <div class="d-flex justify-content-between mb-4">
      <button @click="logout" class="btn btn-danger mx-1">Logout</button>
    </div>
  </nav>

    <div class="container my-5">
      <h1 class="text-center mb-4">Completed Service Requests</h1>
      <div class="card shadow-sm">
        <div class="card-body p-4" style="background-color: #e0f7fa;">
          <table class="table table-hover table-bordered">
            <thead class="table-dark">
              <tr>
                <th scope="col">ID</th>
                <th scope="col">Customer ID</th>
                <th scope="col">Customer Name</th>
                <th scope="col">Date of Request</th>
                <th scope="col">Description</th>
                <th scope="col">Price</th>
                <th scope="col">Status</th>
                <th scope="col">Remarks</th>
                <th scope="col">Rating</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in completedServiceRequests" :key="request.id">
                <td>{{ request.id }}</td>
                <td>{{ request.customer_id }}</td>
                <td>{{ request.customer_name }}</td>
                <td>{{ request.date_of_request }}</td>
                <td>{{ request.description }}</td>
                <td>{{ request.price}}</td>
                <td><span :class="statusClass(request.status)">{{ request.status }}</span></td>
                <td>{{ request.remarks }}</td>
                <td>{{ request.rating }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        completedServiceRequests: [],
      };
    },
    async mounted() {
      const customerId = localStorage.getItem("customerId");
      await this.fetchCompletedRequests(customerId);
    },
    methods: {
      logout(){
      localStorage.removeItem('customerId');
      localStorage.removeItem('jwtToken')
      this.$router.push({ name: 'IndexFirst' });
     },
      async fetchCompletedRequests(customerId) {
        const token=localStorage.getItem('jwtToken')
        if(!token){
          alert('You are not logged in, Redirecting you to the logged in page')
          this.$router.push({'name':'CustomerLogin'})
          return;
        }
        const response = await fetch(
          `http://localhost:8000/api/service_requests/completed/${customerId}`,{
            'headers':{
              'Content-Type':'application/json',
              'Authorization':`Bearer ${token}`
            }
          }
        );
        if (response.ok) {
          this.completedServiceRequests = await response.json();
        } else {
          console.error("Failed to fetch completed service requests");
        }
      },
      statusClass(status) {
        switch (status) {
          case "closed":
            return "badge bg-success";
          case "assigned":
            return "badge bg-primary";
          case "rejected":
            return "badge bg-danger";
          default:
            return "badge bg-secondary";
        }
      },
      goToCustomerDashboard(){
        this.$router.push({"name":"CustomerDashboard"})
     },
    },
    filters: {
      currency(value) {
        return "₹" + parseFloat(value).toFixed(2);
      }
    },
  };
  </script>
  
  <style>
  .container {
    max-width: 900px;
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
  
}
  .table-hover tbody tr:hover {
    background-color: #f1f1f1;
  }
  .badge {
    font-size: 0.9rem;
    padding: 0.5em 0.75em;
  }
  </style>