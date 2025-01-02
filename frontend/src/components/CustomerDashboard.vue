<template>
  <nav class="navbar navbar-expand-lg bg-primary mb-4">
    <div class="container-fluid">
      <a class="navbar-brand text-white" href="#">HomeFix | Customer Dashboard</a>
      <div class="d-flex align-items-center">
        <button @click="goToProfilePage" class="btn btn-danger me-2">Your Profile</button>
        <button @click="goToDocumentPage" class="btn btn-light me-2">Documents</button>
        <button @click="goToUpdate" class="btn btn-primary me-2">Update Service Request</button>
        
        <div class="dropdown me-2">
          <button class="btn btn-warning dropdown-toggle" type="button" id="packagesDropdown" data-bs-toggle="dropdown" aria-expanded="false">
            Packages
          </button>
          <ul class="dropdown-menu" aria-labelledby="packagesDropdown">
            <li><a class="dropdown-item" @click="goToHomeFixPackage">HomeFix Package</a></li>
            <li><a class="dropdown-item" @click="goToServicePackages">Professional Packages</a></li>
          </ul>
        </div>

        <div class="dropdown me-2">
          <button class="btn btn-success dropdown-toggle" type="button" id="requestedServicesDropdown" data-bs-toggle="dropdown" aria-expanded="false">
            Requested Services
          </button>
          <ul class="dropdown-menu" aria-labelledby="requestedServicesDropdown">
            <li><a class="dropdown-item" @click="goToActiveRequests('ActiveServiceRequests')">Service Requests</a></li>
            <li><a class="dropdown-item" @click="goToActiveRequests('ActiveServicePackages')">Professional Packages</a></li>
            <li><a class="dropdown-item" @click="goToActiveRequests('ActiveHomeFixPackages')">HomeFix Packages</a></li>
          </ul>
        </div>

        <div class="dropdown me-2">
          <button class="btn btn-secondary dropdown-toggle" type="button" id="completedRequestsDropdown" data-bs-toggle="dropdown" aria-expanded="false">
            Completed Requests
          </button>
          <ul class="dropdown-menu" aria-labelledby="completedRequestsDropdown">
            <li><a class="dropdown-item" @click="goToCompletedRequests('serviceRequests')">Service Requests</a></li>
            <li><a class="dropdown-item" @click="goToCompletedRequests('servicePackages')">Professional Packages</a></li>
            <li><a class="dropdown-item" @click="goToCompletedRequests('homefixPackages')">HomeFix Packages</a></li>
          </ul>
        </div>

        <button @click="logout" class="btn btn-danger">Logout</button>
      </div>
    </div>
  </nav>

  <div class="container mt-5">
    <h1 class="text-center mb-4">Service Options</h1>
    <div class="row">
      <div class="col-md-4 mb-4" v-for="(service, index) in services" :key="index">
        <div class="card shadow-sm service-card">
          <img :src="service.image" class="card-img-top service-image" alt="Service Image">
          <div class="card-body text-center">
            <h5 class="card-title">{{ service.name }}</h5>
            <router-link :to="{name:'ServiceRequest',params:{serviceName:service.name}}">
              <button class="btn btn-primary">Book Now</button>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
export default {
  data() {
    return {
      services: [
        { name: 'Carpenter', image: '/images/carpenter.jpeg' },
        { name: 'Plumber', image: '/images/plumber.jpeg' },
        { name: 'AC Repair', image: '/images/ac_repair.jpg' },
        { name: 'Saloon', image: '/images/saloon.webp' },
        { name: 'Cleaner', image: '/images/cleaner.jpg' },
        { name: 'Painter', image: '/images/painter.jpg' },
      ],
    };
  },
  methods: {
    logout(){
      localStorage.removeItem('customerId');
      localStorage.removeItem('jwtToken')
      this.$router.push({ name: 'IndexFirst' });
    },
    goToServicePackages(){
      this.$router.push({name:'ShowCustomerPackage'})
    },
    goToDocumentPage(){
      this.$router.push({'name':'DocumentsPage'})
    },
    goToHomeFixPackage(){
      this.$router.push({'name':'HomeFixPackage'})
    },
    goToCompletedRequests(type){
      this.$router.push({'name':type})
    },
    goToActiveRequests(type){
      this.$router.push({'name':type})
    },
    goToProfilePage(){
      this.$router.push({'name':'UpdateCustomerProfile'})
    },
    goToUpdate(){
      this.$router.push({'name':'UpdateServiceRequest'})
    },
  },
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

.service-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-bottom: 3px solid #007bff;
}

.service-card {
  transition: transform 0.3s, box-shadow 0.3s;
}
.service-card:hover {
  transform: translateY(-5px);
  box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.1);
}

.footer {
  background-color: #f8f9fa;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}
</style>