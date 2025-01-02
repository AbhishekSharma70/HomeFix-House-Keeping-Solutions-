<template>
  <nav class="navbar navbar-expand-lg bg-primary mb-4">
    <div class="container-fluid">
      <a class="navbar-brand text-white" href="#">HomeFix | Professional Dashboard</a>
    </div>
    <div class="d-flex align-items-center">
    <div class="dropdown me-2">
          <button class="btn btn-secondary btn-mid dropdown-toggle custom-btn" type="button" id="completedRequestsDropdown" data-bs-toggle="dropdown" aria-expanded="false">
            Completed Requests
          </button>
          <ul class="dropdown-menu" aria-labelledby="completedRequestsDropdown">
            <li><a class="dropdown-item" @click="goToCompletedProfessionalRequests('professionalserviceRequests')">Service Requests</a></li>
            <li><a class="dropdown-item" @click="goToCompletedProfessionalRequests('professionalservicePackages')">Professional Packages</a></li>
            <li><a class="dropdown-item" @click="goToCompletedProfessionalRequests('professionalhomefixPackages')">HomeFix Packages</a></li>
          </ul>
        </div>
    
    <button @click="yourprofile" class="btn btn-danger btn-mid mx-1 custom-btn">Your Profile</button>
    <button @click="yourservicepackages" class="btn btn-success btn-mid mx-1 custom-btn">Your Packages</button>
    <button @click="goToCreatePackage" class="btn btn-primary btn-mid mx-1 custom-btn">Create Service Package</button>
    <button @click="logout" class="btn btn-danger btn-mid mx-1 custom-btn">Logout</button>
    </div>
  </nav>

  <div class="container mt-5">
    <h2 class="text-center mb-4">Incoming Service Requests</h2>
    <div v-if="serviceRequests.length === 0" class="alert alert-info">
      No incoming service requests.
    </div>
    <div class="table-responsive" v-else>
      <table class="table  table-hover table-striped align-middle">
        <thead>
          <tr>
            
            
            <th>Customer Name</th>
            <th>Phone Number</th>
            <th>Description</th>
            <th>Remarks</th>
            <th>Status</th>
            <th>Date of Request</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in serviceRequests" :key="request.id">
            
            
            <td>{{ request.customer_name }}</td>
            <td>{{ request.phone_number }}</td>
            <td>{{ request.description }}</td>
            <td>{{ request.remarks }}</td>
            <td>{{ request.status }}</td>
            <td>{{ request.date_of_request }}</td>
            <td>
              <button class="btn btn-success" @click="acceptRequest(request.id)" :disabled="request.status !== 'requested'">
                Accept
              </button>
              <button class="btn btn-danger" @click="rejectRequest(request.id)" :disabled="request.status !== 'requested'">
                Reject
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <br>
  <br>

  <div class="container mt-5">
    <h2 class="text-center mb-4">Incoming Booked Service Packages</h2>
    <div v-if="bookedPackages.length === 0" class="alert alert-info">No incoming packages booked.</div>
    <div class="table-responsive" v-else>
      <table class="table  table-hover table-striped align-middle">
        <thead>
          <tr>
            <th>Package ID</th>
            <th>Package Name</th>
            <th>Customer ID</th>
            <th>Customer Name</th>
            <th>Address</th>
            <th>Phone Number</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="pkg in bookedPackages" :key="pkg.package_id">
            <td>{{ pkg.package_id }}</td>
            <td>{{ pkg.package_name }}</td>
            <td>{{ pkg.customer_id }}</td>
            <td>{{ pkg.customer_name }}</td>
            <td>{{ pkg.address }}</td>
            <td>{{ pkg.phone_number }}</td>
            <td>{{ pkg.status }}</td>
            <td>
            <button class="btn btn-success" @click="acceptPackage(pkg.id)" :disabled="pkg.status!=='pending'">Accept</button>
            <button class="btn btn-danger" @click="rejectPackage(pkg.id)" :disabled="pkg.status!=='pending'">Reject</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <br>
  <br>

  <div class="container mt-5">
    <h2 class="text-center mb-4">Incoming Booked HomeFix Packages</h2>
    <br>
    <div v-if="adminPackages.length === 0" class="alert alert-info">No incoming homefix packages booked.</div>
    <div class="table-responsive" v-else>
      <table class="table  table-hover table-striped align-middle">
        <thead>
          <tr>
            <th>Package Name</th>
            <th>Customer ID</th>
            <th>Customer Name</th>
            <th>Phone Number</th>
            <th>Date of Request</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="pkg in adminPackages" :key="pkg.id">
            <td>{{ pkg.package_name }}</td>
            <td>{{ pkg.customer_id }}</td>
            <td>{{ pkg.customer_name }}</td>
            <td>{{ pkg.customer_phone_number }}</td>
            <td>{{ pkg.date_of_request }}</td>
            <td>{{ pkg.status }}</td>
            <td>
              <button  
                @click="updatePackageStatus(pkg.id, 'assigned')" 
                class="btn btn-success mx-1"
                :disabled="pkg.status !== 'requested'"
              >
                Accept
              </button>
              <button 
                @click="updatePackageStatus(pkg.id, 'rejected')" 
                class="btn btn-danger mx-1"
                :disabled="pkg.status !== 'requested'"
              >
                Reject
              </button>
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
      serviceRequests: [],
      bookedPackages: [],
      adminPackages:[]
    };
  },
  created() {
    this.fetchServiceRequests();
    this.fetchBookedPackages();
    this.fetchAdminPackages();
  },
  methods: {
    logout() {
      localStorage.removeItem('professionalId');
      localStorage.removeItem('jwtToken')
      this.$router.push({ name: 'IndexFirst' });
    },
    async fetchServiceRequests() {
      const token=localStorage.getItem('jwtToken')
      if(!token){
        alert('You are not logged in,Redirecting you to the login page.')
        this.$router.push({'name':'ServiceProfessionalLogin'})
        return;
      }
      const professionalId = localStorage.getItem('professionalId');
      try {
        const response = await fetch(`http://localhost:8000/api/service_professional_requests/${professionalId}`,{
          headers:{
            'Content-Type':'application/json',
            'Authorization':`Bearer ${token}`
          }
        });
        const data = await response.json();
        if (response.ok) {
          this.serviceRequests = data.service_requests;
        } else {
          console.log("Not found")
        }
      } catch (error) {
        console.error('Error fetching service requests:', error);
      }
    },

    async acceptRequest(requestId) {
      const token=localStorage.getItem('jwtToken')
      if(!token){
        alert('You are not logged in,Redirecting you to the login page.')
        this.$router.push({'name':'ServiceProfessionalLogin'})
        return;
      }
      try {

        let professionalLatitude = null;
        let professionalLongitude = null;

        // Function to get the professional's current location
        const getLocation = () => {
            return new Promise((resolve, reject) => {
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(
                        (position) => {
                            professionalLatitude = position.coords.latitude;
                            professionalLongitude = position.coords.longitude;
                            resolve();  // Resolving once the location is fetched
                        },
                        (error) => {
                            console.error("Error fetching the location: ", error);
                            alert("Unable to fetch location. Please check your permission.");
                            reject("Location fetch failed");
                        }
                    );
                } else {
                    alert('Geolocation is not supported by this browser');
                    reject("Geolocation not supported");
                }
            });
        };

        // Get the professional's location
        await getLocation();
      

       const customerResponse=await fetch(`http://localhost:8000/api/service_requests/${requestId}/location`,{
        method:'GET',
        headers:{
          'Authorization':`Bearer ${token}`,
          'Content-Type':'application/json'
        }
       });

       if(!customerResponse.ok){
        alert('Failed to retreive the customer location')
        return;
       }

       const customerData=await customerResponse.json()
       const customerLatitude=customerData.location.latitude
       console.log(customerLatitude)
       const customerLongitude=customerData.location.longitude
       console.log(customerLongitude)


       const isNearby = (lat1,lon1,lat2,lon2,threshold=0.1)=>{
        const latDiff=Math.abs(lat1-lat2)
        const lonDiff=Math.abs(lon1-lon2)
        return (latDiff<=threshold && lonDiff<=threshold)
       }

       if(!isNearby(professionalLatitude,professionalLongitude,customerLatitude,customerLongitude)){
        alert('Please be in the customer\'s location to continue with the request .')
        return;
       }
      
       const response = await fetch(`http://localhost:8000/api/service_requests/${requestId}/accept`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json',
          'Authorization':`Bearer ${token}`
         },
        body: JSON.stringify({
          service_status: 'assigned' // Updating the status to 'assigned'
        })
      });
       if (response.ok) {
        alert('Service request accepted');
        this.fetchServiceRequests(); // Refresh the list of service requests
       } else {
        alert('Failed to accept service request');
       }
     } catch (error) {
      console.error('Error accepting request:', error);
     }
  },
  async rejectRequest(requestId) {
    const token=localStorage.getItem('jwtToken')
      if(!token){
        alert('You are not logged in,Redirecting you to the login page.')
        this.$router.push({'name':'ServiceProfessionalLogin'})
        return;
      }
    try {
      const response = await fetch(`http://localhost:8000/api/service_requests/${requestId}/reject`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json',
          'Authorization':`Bearer ${token}`
         },
        body: JSON.stringify({
          service_status: 'rejected' // Updating the status to 'rejected'
        })
      });
      if (response.ok) {
        alert('Service request rejected');
        this.fetchServiceRequests(); // Refresh the list of service requests
      } else {
        alert('Failed to reject service request');
      }
    } catch (error) {
      console.error('Error rejecting request:', error);
    }
  },
  async fetchBookedPackages() {
    const token=localStorage.getItem('jwtToken')
      if(!token){
        alert('You are not logged in,Redirecting you to the login page.')
        this.$router.push({'name':'ServiceProfessionalLogin'})
        return;
      }
    const professionalId = localStorage.getItem('professionalId');
    try {
      const response = await fetch(`http://localhost:8000/api/professional_booked_packages/${professionalId}`,{
        headers:{
          'Content-Type':'application/json',
          'Authorization':`Bearer ${token}`
        }
      });
      const data = await response.json();
      this.bookedPackages = data.booked_packages;
    } catch (error) {
      console.error('Error fetching booked packages:', error);
      }
    },
  goToCreatePackage(){
    this.$router.push({name:'CreateServicePackage'});
  },
  async acceptPackage(bookedServiceRequestId) {
    const token=localStorage.getItem('jwtToken')
      if(!token){
        alert('You are not logged in,Redirecting you to the login page.')
        this.$router.push({'name':'ServiceProfessionalLogin'})
        return;
      }
    try {


        let professionalLatitude = null;
        let professionalLongitude = null;

        // Function to get the professional's current location
        const getLocation = () => {
            return new Promise((resolve, reject) => {
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(
                        (position) => {
                            professionalLatitude = position.coords.latitude;
                            professionalLongitude = position.coords.longitude;
                            resolve();  // Resolving once the location is fetched
                        },
                        (error) => {
                            console.error("Error fetching the location: ", error);
                            alert("Unable to fetch location. Please check your permission.");
                            reject("Location fetch failed");
                        }
                    );
                } else {
                    alert('Geolocation is not supported by this browser');
                    reject("Geolocation not supported");
                }
            });
        };

        // Get the professional's location
        await getLocation();

        const customerResponse=await fetch(`http://localhost:8000/api/booked_packages/${bookedServiceRequestId}/location`,{
        method:'GET',
        headers:{
          'Authorization':`Bearer ${token}`,
          'Content-Type':'application/json'
        }
       });

       if(!customerResponse.ok){
        alert('Failed to retreive the customer location')
        return;
       }

       const customerData=await customerResponse.json()
       const customerLatitude=customerData.location.latitude
       console.log(customerLatitude)
       const customerLongitude=customerData.location.longitude
       console.log(customerLongitude)


       const isNearby = (lat1,lon1,lat2,lon2,threshold=0.1)=>{
        const latDiff=Math.abs(lat1-lat2)
        const lonDiff=Math.abs(lon1-lon2)
        return (latDiff<=threshold && lonDiff<=threshold)
       }

       if(!isNearby(professionalLatitude,professionalLongitude,customerLatitude,customerLongitude)){
        alert('Please be in the customer\'s location to continue with the request .')
        return;
       }

        const response = await fetch(`http://localhost:8000/api/booked_service_packages/${bookedServiceRequestId}/accept`, {
            method: 'PATCH',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization':`Bearer ${token}`
            },
            body: JSON.stringify({ 
                service_status: 'accepted' // Set the status to 'accepted'
            })
        });

        if (response.ok) {
            alert('Package accepted. The customer will be notified.');
            this.fetchBookedPackages(); // Refresh the list of booked packages
        } else {
            const errorData = await response.json();
            console.error('Failed to accept package:', errorData);
            alert('Failed to accept package: ' + errorData.message);
        }
    } catch (error) {
        console.error('Error accepting package:', error);
    }
  },
  async rejectPackage(bookedServiceRequestId) {
    const token=localStorage.getItem('jwtToken')
      if(!token){
        alert('You are not logged in,Redirecting you to the login page.')
        this.$router.push({'name':'ServiceProfessionalLogin'})
        return;
      }
    try {
        const response = await fetch(`http://localhost:8000/api/booked_service_packages/${bookedServiceRequestId}/reject`, {
            method: 'PATCH',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization':`Bearer ${token}`
            },
            body: JSON.stringify({ 
                service_status: 'rejected'  // Set status to 'rejected'
            })
        });

        if (response.ok) {
            alert('Package rejected. The customer will be notified.');
            this.fetchBookedPackages();  // Refresh the list of booked packages
        } else {
            const errorData = await response.json();
            alert('Failed to reject package: ' + errorData.message);
        }
    } catch (error) {
        console.error('Error rejecting package:', error);
    }
   },
   async fetchAdminPackages() {
      const token=localStorage.getItem('jwtToken')
      if(!token){
        alert('You are not logged in,Redirecting you to the login page.')
        this.$router.push({'name':'ServiceProfessionalLogin'})
        return;
      }
      const professionalId = localStorage.getItem('professionalId'); // Assuming professional ID is stored in localStorage

      try {
        const response = await fetch(`http://localhost:8000/api/professional_packages/${professionalId}`,{
          headers:{
            'Content-Type':'application/json',
            'Authorization':`Bearer ${token}`
          }
        });
        if (!response.ok) {
          throw new Error('Failed to fetch packages');
        }
        const data = await response.json();
        this.adminPackages = data;
      } catch (error) {
        console.error('Error fetching packages:', error);
      }
    },
    async updatePackageStatus(packageId, status) {
      const token=localStorage.getItem('jwtToken')
      if(!token){
        alert('You are not logged in,Redirecting you to the login page.')
        this.$router.push({'name':'ServiceProfessionalLogin'})
        return;
      }
      if(status=='assigned'){

        let professionalLatitude = null;
        let professionalLongitude = null;

        // Function to get the professional's current location
        const getLocation = () => {
            return new Promise((resolve, reject) => {
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(
                        (position) => {
                            professionalLatitude = position.coords.latitude;
                            professionalLongitude = position.coords.longitude;
                            resolve();  // Resolving once the location is fetched
                        },
                        (error) => {
                            console.error("Error fetching the location: ", error);
                            alert("Unable to fetch location. Please check your permission.");
                            reject("Location fetch failed");
                        }
                    );
                } else {
                    alert('Geolocation is not supported by this browser');
                    reject("Geolocation not supported");
                }
            });
        };

        // Get the professional's location
        await getLocation();
      

       const customerResponse=await fetch(`http://localhost:8000/api/admin_requests/${packageId}/location`,{
        method:'GET',
        headers:{
          'Authorization':`Bearer ${token}`,
          'Content-Type':'application/json'
        }
       });

       if(!customerResponse.ok){
        alert('Failed to retreive the customer location')
        return;
       }

       const customerData=await customerResponse.json()
       const customerLatitude=customerData.location.latitude
       console.log(customerLatitude)
       const customerLongitude=customerData.location.longitude
       console.log(customerLongitude)


       const isNearby = (lat1,lon1,lat2,lon2,threshold=0.1)=>{
        const latDiff=Math.abs(lat1-lat2)
        const lonDiff=Math.abs(lon1-lon2)
        return (latDiff<=threshold && lonDiff<=threshold)
       }

       if(!isNearby(professionalLatitude,professionalLongitude,customerLatitude,customerLongitude)){
        alert('Please be in the customer\'s location to continue with the request .')
        return;
       }
      }
      const updateData = {
        package_id: packageId,
        status: status,
      };

      try {
        const response = await fetch('http://localhost:8000/api/update_package_status', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization':`Bearer ${token}`
          },
          body: JSON.stringify(updateData),
        });

        const data = await response.json();
        alert(data.message);
        this.fetchProfessionalPackages(); // Refresh the packages list after status update
      } catch (error) {
        console.error('Error updating package status:', error);
      }
    },
    goToCompletedProfessionalRequests(type){
      this.$router.push({'name':type})
    },
    yourservicepackages(){
      this.$router.push({'name':'ServiceProfessionalPackage'})
    },
    yourprofile(){
      this.$router.push({'name':'UpdateProfessionalProfile'})
    }
  }
};
</script>

<style>
.custom-btn  {
  width:190px;
  height:60px

}
</style>
    