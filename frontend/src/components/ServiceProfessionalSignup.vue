<template>
  <nav class="navbar navbar-expand-lg mb-4 shadow-sm bg-primary text-white" >
    <div class="container-fluid">
      <a class="navbar-brand text-white" @click="goToIndex">HomeFix | Service Professional Signup</a>
    </div>
  </nav>
  <div class="container-fluid d-flex justify-content-center align-items-center mt-3" style="min-height: 80vh; padding-top: 0;" id="app">
    <div class="card p-4" style="background-color: #e0f7fa; max-width: 400px; width: 100%;">
      <div class="card-body">
        <h2>Service Professional Signup</h2>

        <form method="POST" enctype="multipart/form-data" @submit.prevent="submitSignup">
          <div>
            <label for="username">Username:</label>
            <input class="form-control w-100 mx-auto" type="text" id="username" v-model="username" placeholder="Enter Username" required />
          </div>
          <br>

          <div>
            <label for="password">Password:</label>
            <input class="form-control w-100 mx-auto" type="password" id="password" v-model="password" placeholder="Enter Password" required />
          </div>
          <br>

          <div>
            <label for="fullname">Full Name:</label>
            <input class="form-control w-100 mx-auto" type="text" id="fullname" v-model="fullname" placeholder="Enter Full Name" required />
          </div>
          <br>

          <div>
            <label for="serviceType">Service Type:</label>
            <select id="serviceType" v-model="service_type" class="form-control w-100 mx-auto" required>
              <option value="">Select Service Type</option>
              <option value="Carpenter">Carpenter</option>
              <option value="Plumber">Plumber</option>
              <option value="AC Repair">AC Repair</option>
              <option value="Saloon">Saloon</option>
              <option value="Cleaner">Cleaner</option>
              <option value="Painter">Painter</option>
            </select>
          </div>
          <br>

          <div>
            <label for="experience">Experience:</label>
            <input class="form-control w-100 mx-auto" type="text" id="experience" v-model="experience" placeholder="Enter Experience" required />
          </div>
          <br>

          <div>
            <label for="document">Attach Document (PDF):</label>
            <input class="form-control w-100 mx-auto" type="file" id="document" @change="handleFileUpload" required />
          </div>
          <br>

          <div>
            <label for="phone_number">Enter Phone Number:</label>
            <input class="form-control w-100 mx-auto" type="text" id="phone_number" v-model="phone_number" placeholder="Enter Phone Number" required />
          </div>
          <br>

          <div>
            <label for="address">Address:</label>
            <input class="form-control w-100 mx-auto" type="text" id="address" v-model="address" placeholder="Enter Address" required />
          </div>
          <br>

          <div>
            <label for="pincode">Pincode:</label>
            <input class="form-control w-100 mx-auto" type="text" id="pincode" v-model="pincode" placeholder="Enter Pincode" required />
          </div>
          <br>

          <button class="btn btn-success" type="submit">Signup</button>
        </form>
        <br>

        <div v-if="message" :class="{'error-message': isError, 'success-message': !isError}">
          {{ message }}
        </div>
        <p class="mt-2">
          Already have an account? <router-link to="/serviceprofessional_login">Login here</router-link>
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
      fullname: '',
      service_type: '',
      experience: '',
      document: null,
      phone_number: '',
      address: '',
      pincode: '',
      message: '',
      isError: false,
    };
  },
  methods: {
    handleFileUpload(event) {
      this.document = event.target.files[0];
    },
    submitSignup() {
      const formData = new FormData();
      formData.append('username', this.username);
      formData.append('password', this.password);
      formData.append('fullname', this.fullname);
      formData.append('service_type', this.service_type);
      formData.append('experience', this.experience);
      formData.append('document', this.document);
      formData.append('phone_number', this.phone_number);
      formData.append('address', this.address);
      formData.append('pincode', this.pincode);

      fetch('http://localhost:8000/api/service_professional_signup', {
        method: 'POST',
        body: formData,
      })
        .then(response => response.json())
        .then(data => {
          if (data.message === 'Signup successful!') {
            this.message = 'Signup successful!';
            this.isError = false;
          } else {
            this.message = 'Signup Failed: ' + data.message;
            this.isError = true;
          }
        })
        .catch(error => {
          this.message = 'Error: ' + error.message;
          this.isError = true;
        });
    },
    goToIndex(){
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

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 10px;
  border: 1px solid #f5c6cb;
  border-radius: 5px;
  margin-top: 10px;
  width: 300px;
}

.success-message {
  background-color: #d4edda;
  color: #155724;
  padding: 10px;
  border: 1px solid #c3e6cb;
  border-radius: 5px;
  margin-top: 10px;
  width: 300px;
}

</style>