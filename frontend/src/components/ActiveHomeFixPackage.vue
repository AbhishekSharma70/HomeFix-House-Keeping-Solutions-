<template>

<nav class="navbar navbar-expand-lg bg-body-tertiary mb-0">
    <div class="container-fluid">
        <a class="navbar-brand text-white" @click="goToCustomerDashboard">HomeFix | HomeFix Packages</a>
    </div>
    <button @click="logout" class="btn btn-danger mx-1">Logout</button>
</nav>

<div class="container mt-5">
    <h2 class="text-center mb-4">Your Booked HomeFix Packages</h2>
    <div v-if="bookedAdminPackages.length === 0" class="alert alert-info">No booked packages.</div>
    <div v-else>
      <table class="table table-striped">
        <thead>
          <tr>
            <th>Package ID</th>
            <th>Package Name</th>
            <th>Status</th>
            <th>Date of Request</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="pkg in bookedAdminPackages" :key="pkg.package_id">
            <td>{{ pkg.package_id }}</td>
            <td>{{ pkg.package_name }}</td>
            <td>{{ pkg.status }}</td>
            <td>{{ pkg.date_of_request }}</td>
            <td>
              <button 
                v-if="pkg.status === 'assigned'" 
                @click="closeAdminPackage(pkg.id)" 
                class="btn btn-success"
              >
                Close 
              </button>
              <span v-else>{{ pkg.status }}</span>
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
      remarks:'',
      rating:'',
      bookedAdminPackages:[]
    };
  },
  created(){
    this.fetchBookedAdminPackages();
  },
  methods: {
    logout(){
      localStorage.removeItem('customerId');
      localStorage.removeItem('jwtToken')
      this.$router.push({ name: 'IndexFirst' });
    },
    closeAdminPackage(pkgId){
      this.$router.push({'name':'CloseAdminPackage',params:{pkgId}})
    },
    async fetchBookedAdminPackages() {
      const token=localStorage.getItem('jwtToken')
      if(!token){
        alert('You are not logged in. Redirecting you to the login page')
        this.$router.push({'name':'CustomerLogin'})
        return;
      }
      const customerId = localStorage.getItem('customerId'); // Replace with the actual logged-in customer ID
      try {
        const response = await fetch(`http://localhost:8000/api/customer_booked_packages/${customerId}`,{
          'headers':{
            'Content-Type':'application/json',
            'Authorization':`Bearer ${token}`
          }
        });
        const data = await response.json();
        if (response.ok) {
          this.bookedAdminPackages = data
        } else {
          console.log(data.error || 'Failed to fetch booked packages.');
        }
      } catch (error) {
        console.error('Error fetching booked packages:', error);
      }
    },
    goToCustomerDashboard(){
      this.$router.push({'name':'CustomerDashboard'})
    }
  }
} ;
</script>

<style scoped>
.service-image{
  width:100%;
  height:200px;
  object-fit:cover
}
</style>