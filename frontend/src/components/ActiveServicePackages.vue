<template>

<nav class="navbar navbar-expand-lg bg-body-tertiary mb-0">
    <div class="container-fluid">
        <a class="navbar-brand text-white" @click="goToCustomerDashboard">HomeFix | Service Packages</a>
    </div>
    <button @click="logout" class="btn btn-danger mx-1">Logout</button>
</nav>

     <div class="container mt-5">
    <h2 class="text-center mb-4">Your Active Booked Packages</h2>
      <table class="table table-striped">
        <thead>
          <tr>
            <th>Package ID</th>
            <th>Package Name</th>
            <th>Description</th>
            <th>Professional Name</th>
            <th>Phone Number</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="pkg in bookedPackages" :key="pkg.id">
            <td>{{ pkg.package_id }}</td>
            <td>{{ pkg.package_name }}</td>
            <td>{{ pkg.description }}</td>
            <td>{{ pkg.professional_name }}</td>
            <td>{{ pkg.phone_number }}</td>
            <td>{{ pkg.status }}</td>
            <td><button v-if="pkg.status==='accepted'" @click="closePackage(pkg.id)" class="btn btn-success">Close</button></td>
          </tr>
        </tbody>
      </table>
    </div>
    <br>

</template>

<script>
export default {
  data() {
    return {
    
      remarks:'',
      rating:'',
      bookedPackages:[],

    };
  },
  created(){
    this.fetchBookedPackages();
  },
  methods: {
    logout(){
      localStorage.removeItem('customerId');
      localStorage.removeItem('jwtToken')
      this.$router.push({ name: 'IndexFirst' });
    },
    async fetchBookedPackages() {
      const token=localStorage.getItem('jwtToken')
      if(!token){
        alert('You are not logged in. Redirecting you to login page')
        return;
      }
      const customerId = localStorage.getItem('customerId'); // Replace with the actual logged-in customer ID
      try {
        const response = await fetch(`http://localhost:8000/api/booked_service_packages/customer/${customerId}`,{
          'headers':{
            'Content-Type':'application/json',
            'Authorization':`Bearer ${token}`
          }
        });
        const data = await response.json();
        if (response.ok) {
          this.bookedPackages = data.accepted_packages;
        } else {
          console.log(data.error || 'Failed to fetch booked packages.');
        }
      } catch (error) {
        console.error('Error fetching booked packages:', error);
      }
    },
    closePackage(pkgId){
      this.$router.push({name:'ClosePackage',params:{pkgId}});
    },
    goToCustomerDashboard(){
      this.$router.push({'name':'CustomerDashboard'})
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