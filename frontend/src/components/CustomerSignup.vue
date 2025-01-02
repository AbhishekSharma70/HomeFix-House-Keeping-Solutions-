<template>
  <nav class="navbar navbar-expand-lg mb-4 shadow-sm bg-primary text-white">
    <div class="container-fluid">
      <a class="navbar-brand text-white" @click="goToindex">HomeFix | Customer Signup</a>
    </div>
  </nav>
  <div
    class="container-fluid d-flex justify-content-center align-items-center mt-0"
    style="height: 100vh; padding-top: 0;"
    id="app"
  >
    <div class="card p-4" style="background-color: #e0f7fa; max-width: 400px; width: 100%;">
      <div class="card-body">
        <h2 class="text-center">Customer Signup</h2>
        <br />
        <form @submit.prevent="submitSignup">
          <div class="form-group">
            <label for="username">Username:</label>
            <input
              class="form-control"
              type="text"
              id="username"
              v-model="username"
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
              v-model="password"
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
              v-model="full_name"
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
              v-model="phone_number"
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
              v-model="address"
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
              v-model="pincode"
              placeholder="Enter Pincode"
              required
            />
          </div>
          <br />

          <div class="form-group">
            <label for="location">Location</label>
            <br>
            <br>
            <button class="btn btn-info" @click="getLocation">Get Home Location</button>
          <br>
          <div v-if="location.latitude && location.longitude" class="mt-2">
            <p>Latitude:{{ location.latitude }}</p>
            <p>longitude:{{ location.longitude }}</p>
          </div>
          </div>
          <br>

          <button class="btn btn-success" type="submit">Signup</button>
        </form>

        <div v-if="message" :class="['message', isError ? 'error-message' : 'success-message']">
          {{ message }}
        </div>
        <br />
        <p class="mt-2">
          Already have an account? <router-link to="/customer_login">Login here</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      full_name: '',
      phone_number: '',
      address: '',
      pincode: '',
      message: '',
      isError: false,
      location:{
        latitude:null,
        longitude:null
      }
    };
  },
  methods: {
    getLocation(){

      if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition((position)=>{
          this.location.latitude=position.coords.latitude;
          this.location.longitude=position.coords.longitude;
        },
        (error)=>{
          console.error("Error fetching the location: ",error)
          alert("Unable to fetch location. Please check your permission")
        }
        );
      }else{
        alert('Geolocation is not supported by this browser')
      }
    },
    submitSignup() {
      if (!this.username || !this.password || !this.full_name || !this.phone_number || !this.address || !this.pincode) {
        this.message = 'Please fill in all fields';
        this.isError = true;
        return;
      }
      fetch('http://localhost:8000/api/customer_signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: this.username,
          password: this.password,
          full_name: this.full_name,
          phone_number: this.phone_number,
          address: this.address,
          pincode: this.pincode,
          longitude:this.location.longitude,
          latitude:this.location.latitude
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.message === 'Signup successful!') {
            this.message = data.message;
            this.isError = false;
            // Redirect after successful signup
            setTimeout(() => {
              window.location.href = '/customer_login';
            }, 2000);
          } else {
            this.message = data.message;
            this.isError = true;
          }
        })
        .catch((error) => {
          this.message = 'Error: ' + error.message;
          this.isError = true;
        });
    },
    goToindex(){
      this.$router.push({'name':'IndexFirst'})
    }
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

.message {
  margin-top: 20px;
  padding: 10px;
  border-radius: 5px;
  width: 100%;
}

.success-message {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}
</style>