<template>
  <nav class="navbar navbar-expand-lg mb-4 shadow-sm bg-primary text-white">
    <div class="container-fluid">
      <a class="navbar-brand text-white" @click="goToIndex" >HomeFix | Admin Signup</a>
    </div>
  </nav>
  <div
    class="container-fluid d-flex justify-content-center align-items-center mt-0"
    style="height: 100vh; padding-top: 0;"
    id="app1"
  >
    <div class="card p-4" style="background-color: #e0f7fa; max-width: 400px; width: 100%;">
      <div class="card-body">
        <h2 class="text-center">Admin Signup</h2>
        <br />
        <form @submit.prevent="signup">
          <div class="form-group">
            <label for="username">Username</label>
            <input
              type="text"
              class="form-control"
              id="username"
              v-model="username"
              placeholder="Enter Username"
              required
            />
          </div>
          <br />
          <div class="form-group">
            <label for="password">Password</label>
            <input
              type="password"
              class="form-control"
              id="password"
              v-model="password"
              placeholder="Enter Password"
              required
            />
          </div>
          <br />
          <button type="submit" class="btn btn-success">Signup</button>
        </form>
        <p v-if="show_message" class="mt-3" :class="messageClass">{{ message1 }}</p>
        <br />
        <p class="mt-2">
          Already have an account? <router-link to="/admin_login">Login here</router-link>
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
      message1: '',
      show_message: false,
      messageClass: '',
    };
  },
  methods: {
    signup() {
      if (!this.username || !this.password) {
        this.message1 = 'Please fill in both fields';
        this.messageClass = 'text-danger';
        this.show_message = true;
        return;
      }
      fetch('http://localhost:8000/api/admin_signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: this.username,
          password: this.password,
        }),
      })
        .then(response => response.json())
        .then(data => {
          if (data.message === "Signup successful!") {
            this.message1 = data.message;
            this.messageClass = 'text-success';
            this.show_message = true;
            setTimeout(() => {
              window.location.href = '/admin_login'; // Redirect after a few seconds
            }, 2000);
          } else {
            this.message1 = data.message;
            this.messageClass = 'text-danger';
            this.show_message = true;
          }
        })
        .catch(error => {
          console.log('Error: ', error);
          this.message1 = 'An error occurred. Please try again.';
          this.messageClass = 'text-danger';
          this.show_message = true;
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


.text-danger {
  color: #dc3545;
}

.text-success {
  color: #28a745;
}
</style>