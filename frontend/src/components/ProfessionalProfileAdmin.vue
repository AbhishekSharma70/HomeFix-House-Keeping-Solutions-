<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary mb-0">
      <div class="container-fluid">
       <a class="navbar-brand text-white" >HomeFix | Service Professional Profile</a>
      </div>
    </nav>

  <div class="container mt-5">
      <h2 class="text-center mb-4">Service Professional Profile</h2>
      <div class="container-fluid d-flex justify-content-center align-items-center mt-0"  id="app">
       <div class="card p-4" style="background-color:#e0f7fa;max-width:400px;width:100%;">
        <div class="card-body"></div>
    <h2>{{ professional.full_name }}</h2>
    <br>
    <p><strong>Service Type:</strong> {{ professional.service_type }}</p>
    <p><strong>Experience:</strong> {{ professional.experience }} years</p>
    <p><strong>Address:</strong> {{ professional.address }}</p>
    <p><strong>Pincode:</strong> {{ professional.pincode }}</p>
  </div>
  </div>
  </div>
</template>

<script>
export default {
    props: {
      id: {
        type: Number,
        required: true
      }
    },
  data() {
    return {
      professional: {},
    };
  },
  created() {
    this.fetchProfessional();
  },
  methods: {
    fetchProfessional() {
      const token=localStorage.getItem('jwtToken')
      if(!token){
        alert('You are not logged in,Redirecting you to the login page')
        this.$router.push({'name':'AdminLogin'})
        return;
      }
      const professionalId = this.$route.params.id;
      fetch(`http://localhost:8000/api/professional/${professionalId}`,{
        headers:{
          'Content-Type':'application/json',
          'Authorization':`Bearer ${token}`
        }
      })
        .then((response) => response.json())
        .then((data) => {
          this.professional = data;
        })
        .catch((error) => {
          console.error('Error fetching professional:', error);
        });
    },
  },
};
</script>