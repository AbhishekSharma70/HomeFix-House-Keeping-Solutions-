<template>
  <nav class="navbar navbar-expand-lg mb-4 shadow-sm bg-primary text-white" >
    <div class="container-fluid">
      <a class="navbar-brand text-white" @click="goToindex">HomeFix | Admin Login</a>
    </div>
  </nav>  
  <div class="container-fluid d-flex justify-content-center align-items-center mt-0" style="height: 100vh; padding-top: 0;" id="app">
    <div class="card p-4" style="background-color: #e0f7fa; max-width: 400px; width: 100%; border-radius: 15px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);">
      <div class="card-body">
        <h2 class="text-center">Admin Login</h2>
        <br>
        <form @submit.prevent="login">
          <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input
              type="text"
              class="form-control"
              id="username"
              v-model="username"
              placeholder="Enter Username"
              required
            />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input
              type="password"
              class="form-control"
              id="password"
              v-model="password"
              placeholder="Enter Password"
              required
            />
          </div>
          <button type="submit" class="btn btn-primary w-100">Login</button>
          <p v-if="message" class="mt-3 text-center" :class="messageClass">{{ message }}</p>
        </form>
        <br>
        <p class="text-center mt-2">
          Don't have an account? <router-link to="/admin_signup">Sign up here</router-link>
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
      message: '',
      messageClass: ''
    };
  },
  methods: {
    login() {
      console.log('Login method called');
      if (!this.username || !this.password) {
        this.message = 'Please fill in both fields';
        this.messageClass = 'text-danger';
        return;
      }
      fetch('http://localhost:8000/api/admin_login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: this.username,
          password: this.password
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.message === 'Login successful!') {
          localStorage.setItem('adminId', data.admin_id);
          localStorage.setItem('isAuthenticated', 'true');
          localStorage.setItem('role', 'Admin');
          localStorage.setItem('jwtToken',data.access_token)
          this.message = data.message;
          this.messageClass = 'text-success';
          setTimeout(() => {
            window.location.href = '/admin_dashboard'; // Redirect to dashboard after login
          }, 2000);
        } else if (data.message === "Invalid credentials!") {
          this.message = data.message;
          this.messageClass = 'text-danger';
        } else {
          this.message = data.message;
          this.messageClass = 'text-danger';
          window.location.href = '/admin_login1'; // Redirect to a different page for invalid login
        }
      })
      .catch(error => {
        console.log('Error:', error);
        this.message = 'An error occurred. Please try again.';
        this.messageClass = 'text-danger';
      });
    },
    goToindex(){
      this.$router.push({'name':'IndexFirst'})
    }
  }
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
  text-align: center;
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