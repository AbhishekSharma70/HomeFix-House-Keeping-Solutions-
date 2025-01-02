<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary mb-0">
      <div class="container-fluid">
       <a class="navbar-brand text-white" @click="goToCustomerDashboard">HomeFix | Service Professional Profile</a>
      </div>
    </nav>
    <div class="container mt-5">
      <h2 class="text-center mb-4">Service Professional Profile</h2>
      <div class="container-fluid d-flex justify-content-center align-items-center mt-0" id="app">
       <div class="card p-4" style="background-color:#e0f7fa;max-width:400px;width:100%;">
        <div class="card-body">
            <div v-if="professional">
        <h3>{{ professional.fullname }}</h3>
        <br>
        <p><strong>Experience:</strong> {{ professional.experience }} years</p>
        <p><strong>Address:</strong> {{ professional.address }}</p>
        <p><strong>Pincode:</strong> {{ professional.pincode }}</p>
      </div>
  
      <div v-else>
        <p>Loading professional details...</p>
      </div>
    </div>
        </div>
       </div>
      </div>
  </template>
  
  <script>
  export default {
    props: {
      professionalId: {
        type: Number,
        required: true
      }
    },
    data() {
      return {
        professional: null,  // Holds the professional's data
        error: null          // Error message if API call fails
      };
    },
    created() {
      this.fetchProfessionalProfile();
    },
    methods: {
      async fetchProfessionalProfile() {
        const token=localStorage.getItem('jwtToken')
        if(!token){
          alert('You are not logged in,Redirecting you to Login Page')
          this.$router.push({'name':'CustomerLogin'})
          return;
        }
        try {
          const response = await fetch(`http://localhost:8000/api/professionals/${this.professionalId}`,{
            headers:{
              'Content-Type':'application/json',
              'Authorization':`Bearer ${token}`
            }
          });
           if (!response.ok) {
            throw new Error('Failed to fetch professional details');
          }
          const data = await response.json();
          this.professional = data;  // Assuming API returns full professional details in response
        } catch (error) {
          console.error('Error fetching professional profile:', error);
          this.error = 'Could not load professional details';
        }
      },
      goToCustomerDashboard(){
        this.$router.push({'name':'CustomerDashboard'})
      }

    }
  };
  </script>