<template>
  <div class="block-management-page">
    <nav class="navbar navbar-expand-lg mb-4 shadow-sm bg-primary text-white fixed-top">
      <div class="container-fluid">
        <a class="navbar-brand text-white" @click="goToAdminDashboard">HomeFix | Block Management</a>
      </div>
    </nav>

    <div class="container" style="margin-top:70px">
      <h1 class="text-center mb-4">Manage User Blocks</h1>

      <br>
      <br>
      
      <h2>Customers</h2>
      <br>
      <br>
      <table class="table table-hover table-striped">
        <thead class="thead-light">
          <tr>
            <th>Customer ID</th>
            <th>Name</th>
            <th>Address</th>
            <th>Pincode</th>
            <th>Block Status</th>
            <th>Views</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="customer in customers" :key="customer.id">
            <td>{{ customer.id }}</td>
            <td>{{ customer.name }}</td>
            <td>{{ customer.address }}</td>
            <td>{{ customer.pincode }}</td>
            <td>
              <button
                :class="{'btn btn-danger': !customer.flagged, 'btn btn-success': customer.flagged}"
                @click="toggleBlock(customer.id, 'customer')"
              >
                {{ customer.flagged ? 'Unblock' : 'Block' }}
              </button>
            </td>
            <td><button class="btn btn-info" @click="goToCustomerView(customer.id)">Views</button></td>
          </tr>
        </tbody>
      </table>

      <br>
      <br>

      <h2>Service Professionals</h2>
      <br>
      <br>
      <table class="table table-hover table-striped">
        <thead class="thead-light">
          <tr>
            <th>Professional ID</th>
            <th>Name</th>
            <th>Service Type</th>
            <th>Address</th>
            <th>Pincode</th>
            <th>Block Status</th>
            <th>Views</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="professional in professionals" :key="professional.id">
            <td>{{ professional.id }}</td>
            <td>{{ professional.name }}</td>
            <td>{{ professional.service_type }}</td>
            <td>{{ professional.address }}</td>
            <td>{{ professional.pincode }}</td>
            <td>
              <button
                :class="{'btn btn-danger': !professional.flagged, 'btn btn-success': professional.flagged}"
                @click="toggleBlock(professional.id, 'professional')"
              >
                {{ professional.flagged ? 'Unblock' : 'Block' }}
              </button>
            </td>
            <td>
              <button @click="goToViews(professional.id)" class="btn btn-info">Views</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      customers: [],
      professionals: [],
    };
  },
  methods: {
    async fetchUsers() {
      const token=localStorage.getItem('jwtToken')
      if(!token){
        alert('You are not logged in,Redirecting you to the login page')
        this.$router.push({'name':'AdminLogin'})
        return;
      }
      const response = await fetch('http://localhost:8000/api/users',{
        headers:{
          'Content-Type':'application/json',
          'Authorization':`Bearer ${token}`
        },
      });
      const data = await response.json();
      this.customers = data.customers;
      this.professionals = data.professionals;
    },
    async toggleBlock(userId, userType) {
      const token=localStorage.getItem('jwtToken')
      if(!token){
        alert('You are not logged in,Redirecting you to the login page')
        this.$router.push({'name':'AdminLogin'})
        return;
      }
      const response = await fetch(`http://localhost:8000/api/users/block/${userId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization':`Bearer ${token}`
        },
        body: JSON.stringify({
          user_type: userType,
        }),
      });
      if (response.ok) {
        alert('Block status updated.');
        this.fetchUsers();  // Refresh the user data
      } else {
        alert('Error updating block status.');
      }
    },
    goToAdminDashboard() {
      this.$router.push({ name: 'AdminDashboard' });
    },
    goToViews(professional_id){
    this.$router.push({name:'ReviewsPage',params: {id:professional_id}})
   },
   goToCustomerView(customer_id){
    this.$router.push({name:'ReviewsCustomerPage',params: {id:customer_id}})
   } 
  },
  mounted() {
    this.fetchUsers();
  },
  
};
</script>

<style scoped>
.block-management-page {
  background-color: #f9f9f9;
  padding: 20px;
  min-height: 100vh;
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

/* Button Styles */
.btn-danger {
  background-color: red;
  color: white;
}

.btn-success {
  background-color: green;
  color: white;
}

/* Table Styling */
.table {
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.table th,
.table td {
  vertical-align: middle;
}

/* Hover Effect for Rows */
.table-hover tbody tr:hover {
  background-color: #e9f7fa; /* Light blue on hover */
}
</style>