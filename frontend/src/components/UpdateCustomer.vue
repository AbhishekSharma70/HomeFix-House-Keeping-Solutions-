<template>
    <nav class="navbar navbar-expand-lg mb-4 shadow-sm bg-primary text-white" >
    <div class="container-fluid">
      <a class="navbar-brand text-white" @click="goToCustomer">HomeFix | Update Customer Profile</a>
    </div>
  </nav>

     <div class="container-fluid d-flex justify-content-center align-items-center mt-3" style="min-height: 80vh; padding-top: 0;" id="app">
    <div class="card p-4" style="background-color: #e0f7fa; max-width: 400px; width: 100%;">
      <div class="card-body">
        <h2>Update Customer Profile</h2>
      <form @submit.prevent="updateCustomerProfile">

          <div class="form-group">
          <label for="username">Username:</label>
            <input
              class="form-control"
              type="text"
              id="username"
              v-model="customer.username"
              placeholder="Enter Username"
              required
            />
          </div>
          <br />

          <div class="form-group">
            <label for="password">Password:</label>
            <input
              class="form-control"
              type="password"
              id="password"
              v-model="customer.password"
              placeholder="Enter Password"
              required
            />
          </div>
          <br />

          <div class="form-group">
            <label for="full_name">Full Name:</label>
            <input
              class="form-control"
              type="text"
              id="full_name"
              v-model="customer.full_name"
              placeholder="Enter Full Name"
              required
            />
          </div>
          <br />

          <div class="form-group">
            <label for="phone_number">Phone Number:</label>
            <input
              class="form-control"
              type="text"
              id="phone_number"
              v-model="customer.phone_number"
              placeholder="Enter Phone Number"
              required
            />
          </div>
          <br />

          <div class="form-group">
            <label for="address">Address:</label>
            <input
              class="form-control"
              type="text"
              id="address"
              v-model="customer.address"
              placeholder="Enter Address"
              required
            />
          </div>
          <br />

          <div class="form-group">
            <label for="pincode">Pincode:</label>
            <input
              class="form-control"
              type="text"
              id="pincode"
              v-model="customer.pincode"
              placeholder="Enter Pincode"
              required
            />
          </div>
          <br />
  
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
        customer: {
          username:'',
          password:'',  
          full_name: '',
          phone_number:'',
          address:'',
          pincode:'',
          
        },
      };
    },
    created() {
      this.fetchCustomerProfile();
    },
    methods: {
      async fetchCustomerProfile() {
        const customerId = localStorage.getItem('customerId');
        const token=localStorage.getItem('jwtToken')
        if(!token){
          alert('You are not logged in. Redirecting to login page')
          this.$router.push({'name':'CustomerLogin'})
          return;
        }
        try {
          const response = await fetch(`http://localhost:8000/api/customers_profile/${customerId}`,{
            headers:{
              'Content-Type':'application/json',
              'Authorization':`Bearer ${token}`
            }
          });
          const data = await response.json();
          this.customer = data.customer_data;
        } catch (error) {
          console.error('Error fetching customer profile:', error);
        }
      },
      async updateCustomerProfile() {
        const token=localStorage.getItem('jwtToken')
        const customerId = localStorage.getItem('customerId');
        if(!token){
          alert('You are not logged in. Redirecting to login page')
          this.$router.push({'name':'CustomerLogin'})
          return;
        }
        try {
          const response = await fetch(`http://localhost:8000/api/customer_update_profile/${customerId}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              'Authorization':`Bearer ${token}`
            },
            body: JSON.stringify(this.customer),
          });
          if (response.ok) {
            alert('Customer profile updated successfully');
            this.$router.push({ name: 'CustomerDashboard' });
          } else {
            alert('Failed to update profile');
          }
        } catch (error) {
          console.error('Error updating customer profile:', error);
        }
      },
      goToCustomer(){
        this.$router.push({'name':'CustomerDashboard'})
      }
    },
  };
  </script>