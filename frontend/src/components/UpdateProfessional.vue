<template>
    <nav class="navbar navbar-expand-lg mb-4 shadow-sm bg-primary text-white" >
    <div class="container-fluid">
      <a class="navbar-brand text-white" @click="goToProfessional">HomeFix | Update Professional Profile</a>
    </div>
  </nav>

    <div class="container-fluid d-flex justify-content-center align-items-center mt-3" style="min-height: 80vh; padding-top: 0;" id="app">
    <div class="card p-4" style="background-color: #e0f7fa; max-width: 400px; width: 100%;">
      <div class="card-body">
        <h2>Update Professional Profile</h2>

      <form @submit.prevent="updateProfessionalProfile">
        <div>
            <label for="username">Username:</label>
            <input class="form-control w-100 mx-auto" type="text" id="username" v-model="professional.username" placeholder="Enter Username" required />
          </div>
          <br>

          <div>
            <label for="password">Password:</label>
            <input class="form-control w-100 mx-auto" type="password" id="password" v-model="professional.password" placeholder="Enter Password" required />
          </div>
          <br>

          <div>
            <label for="fullname">Full Name:</label>
            <input class="form-control w-100 mx-auto" type="text" id="fullname" v-model="professional.fullname" placeholder="Enter Full Name" required />
          </div>
          <br>

          <div>
            <label for="experience">Experience:</label>
            <input class="form-control w-100 mx-auto" type="text" id="experience" v-model="professional.experience" placeholder="Enter Experience" required />
          </div>
          <br>

          <div>
            <label for="phone_number">Enter Phone Number:</label>
            <input class="form-control w-100 mx-auto" type="text" id="phone_number" v-model="professional.phone_number" placeholder="Enter Phone Number" required />
          </div>
          <br>

          <div>
            <label for="address">Address:</label>
            <input class="form-control w-100 mx-auto" type="text" id="address" v-model="professional.address" placeholder="Enter Address" required />
          </div>
          <br>

          <div>
            <label for="pincode">Pincode:</label>
            <input class="form-control w-100 mx-auto" type="text" id="pincode" v-model="professional.pincode" placeholder="Enter Pincode" required />
          </div>
          <br>
  
        <button type="submit" class="btn btn-primary mt-3">Update Profile</button>
      </form>
    </div>
</div>
</div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        professional: {
            username: '',
            password: '',
            fullname: '',
            experience: '',
            phone_number: '',
            address: '',
            pincode: '',
        },
      };
    },
    created() {
      this.fetchProfessionalProfile();
    },
    methods: {
      async fetchProfessionalProfile() {
        const token=localStorage.getItem('jwtToken')
        if(!token){
          alert('You are not logged in,Redirecting you to Login Page.')
          this.$router.push({'name':'ServiceProfessionalLogin'})
          return;
        }
        const professionalId = localStorage.getItem('professionalId')
        try {
          const response = await fetch(`http://localhost:8000/api/service-professionals_profile/${professionalId}`,{
            headers:{
              'Content-Type':'application/json',
              'Authorization':`Bearer ${token}`
            }
          });
          const data = await response.json();
          this.professional = data.professional_data;
        } catch (error) {
          console.error('Error fetching professional profile:', error);
        }
      },
      async updateProfessionalProfile() {
        const token=localStorage.getItem('jwtToken')
        if(!token){
          alert('You are not logged in,Redirecting you to Login Page.')
          this.$router.push({'name':'ServiceProfessionalLogin'})
          return;
        }
        const professionalId = localStorage.getItem('professionalId')
        try {
          const response = await fetch(`http://localhost:8000/api/professional_update_profile/${professionalId}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              'Authorization':`Bearer ${token}`
            },
            body: JSON.stringify(this.professional),
          });
          if (response.ok) {
            alert('Professional profile updated successfully');
            this.$router.push({ name: 'ProfessionalDashboard' });
          } else {
            alert('Failed to update profile');
          }
        } catch (error) {
          console.error('Error updating professional profile:', error);
        }
      },
      goToProfessional(){
        this.$router.push({'name':'ServiceProfessionalDashboard'})
      }
    },
  };
  </script>