<template>
  <nav class="navbar navbar-expand-lg mb-4 shadow-sm bg-primary text-white">
    <div class="container-fluid">
      <a class="navbar-brand text-white" @click="goToindex">HomeFix | Customer Login</a>
    </div>
  </nav>
  <div class="container-fluid d-flex justify-content-center align-items-center mt-0" style="height: 100vh; padding-top: 0;" id="app">
    <div class="card p-4" style="background-color: #e0f7fa; max-width: 400px; width: 100%; border-radius: 15px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);">
      <div class="card-body">
        <h2 class="text-center">Customer Login</h2>
        <br>
        <form @submit.prevent="submitLogin">
          <div class="mb-3">
            <label for="username" class="form-label">Username:</label>
            <input class="form-control" type="text" id="username" v-model="username" placeholder="Enter Username" required />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password:</label>
            <input class="form-control" type="password" id="password" v-model="password" placeholder="Enter Password" required />
          </div>
          <button class="btn btn-primary w-100" type="submit">Login</button>
          <br>
          <div v-if="message" :class="['message', isError ? 'error-message' : 'success-message']">
            {{ message }}
          </div>
        </form>
        <br>
        <p class="text-center mt-2">
          Don't have an account? <router-link to="/customer_signup">Sign up here</router-link>
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
      isError: false,
    };
  },
  methods: {
    submitLogin() {
      if (!this.username || !this.password) {
        this.message = 'Please fill in both fields';
        this.isError = true;
        return;
      }
      fetch('http://localhost:8000/api/customer_login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: this.username,
          password: this.password,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.message === 'Login successful!') {
            localStorage.setItem('customerId', data.customer_id);
            localStorage.setItem('isAuthenticated', 'true');
            localStorage.setItem('role', 'Customer');
            localStorage.setItem('jwtToken',data.access_token)
            this.message = data.message;
            this.isError = false;
            // Redirect after successful login
            window.location.href = '/customer_dashboard';
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