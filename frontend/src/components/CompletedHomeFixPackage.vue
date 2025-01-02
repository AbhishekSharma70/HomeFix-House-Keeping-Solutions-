<template>
    <nav class="navbar navbar-expand-lg mb-4 shadow-sm bg-primary text-white">
    <div class="container-fluid">
      <a class="navbar-brand text-white" @click="goToCustomerDashboard">HomeFix | HomeFix Packages</a>
    </div>
    <div class="d-flex justify-content-between mb-4">
      <button @click="logout" class="btn btn-danger mx-1">Logout</button>
    </div>
  </nav>
  <br>
  <br>
    <div class="container mt-5">
      <h1 class="text-center mb-4">Completed HomeFix Packages</h1>
      <br>
      <div class="card shadow-sm">
        <div class="card-body" style="background-color: #e0f7fa;">
        <table class="table table-bordered">
           <thead class="table-dark">
            <tr>
            <th>Package ID</th>
            <th>Service Name</th>
            <th>Customer ID</th>
            <th>Professional ID</th>
            <th>Professional Name</th>
            <th>Status</th>
            <th>Remarks</th>
            <th>Rating</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="adminPkg in completedAdminServicePackages" :key="adminPkg.id">
            <td>{{ adminPkg.id }}</td>
            <td>{{ adminPkg.name }}</td>
            <td>{{ adminPkg.customer_id }}</td>
            <td>{{ adminPkg.professional_id }}</td>
            <td>{{ adminPkg.professional_name }}</td>
            <td><span :class="statusClass(adminPkg.status)">{{ adminPkg.status }}</span></td>
            <td>{{ adminPkg.remarks }}</td>
            <td>{{ adminPkg.rating }}</td>
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
        completedAdminServicePackages: [],
      };
    },
    async mounted() {
      const customerId = localStorage.getItem('customerId');
      await this.fetchCompletedAdminServicePackages(customerId);
    },
    methods: {
      logout(){
      localStorage.removeItem('customerId');
      localStorage.removeItem('jwtToken')
      this.$router.push({ name: 'IndexFirst' });
    },
      async fetchCompletedAdminServicePackages(customerId) {
        const token=localStorage.getItem('jwtToken')
        if(!token){
          alert('You are not logged in,Redirecting you to the login page')
          this.$router.push({'name':'CustomerLogin'})
          return
        }
        const response = await fetch(`http://localhost:8000/api/booked_admin_service_packages/completed/${customerId}`,{
          'headers':{
            'Content-Type':'application/json',
            'Authorization':`Bearer ${token}`
          }
        });
        if (response.ok) {
          this.completedAdminServicePackages = await response.json();
        } else {
          console.error('Failed to fetch completed admin service packages');
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
        this.$router.push({'name':'CustomerDashboard'})
      }
    },
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
  
}

  .card {
    border: none;
    border-radius: 8px;
  }
  .card-body {
    padding: 1.5rem;
  }
  .table {
    margin-bottom: 0;
    background-color: #ffffff;
  }
  .table thead {
    background-color: #004d40;
    color: #ffffff;
  }
  .table-bordered th,
  .table-bordered td {
    border: 1px solid #004d40;
  }
  .table tbody tr:hover {
    background-color: #e0f2f1;
  }
  h1 {
    font-size: 2rem;
    color: #004d40;
    font-weight: bold;
  }
  </style>