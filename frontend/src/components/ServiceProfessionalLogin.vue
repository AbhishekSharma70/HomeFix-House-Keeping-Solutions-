<template>
  <nav class="navbar navbar-expand-lg mb-4 shadow-sm bg-primary text-white">
    <div class="container-fluid">
      <a class="navbar-brand text-white" @click="goToindex">HomeFix | Service Professional Login</a>
    </div>
  </nav>
  <div
    class="container-fluid d-flex justify-content-center align-items-center mt-0"
    style="height: 100vh; padding-top: 0;"
    id="app"
  >
    <div class="card p-4" style="background-color: #e0f7fa; max-width: 400px; width: 100%;">
      <div class="card-body">
        <h2 class="text-center">Service Professional Login</h2>
        <br />
        <form @submit.prevent="submitLogin">
          <div class="form-group">
            <label for="username">Username:</label>
            <input
              class="form-control w-40 mx-auto"
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
              class="form-control w-40 mx-auto"
              type="password"
              id="password"
              v-model="password"
              placeholder="Enter Password"
              required
            />
          </div>
          <br />
          <button class="btn btn-primary" type="submit">Login</button>
          <div v-if="message" :class="{'error-message': isError, 'success-message': !isError}">
            {{ message }}
          </div>
        </form>
        <br />
        <p class="mt-2">
          Don't have an account? <router-link to="/serviceprofessional_signup">Sign up here</router-link>
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

      fetch('http://localhost:8000/api/service_professional_login', {
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
        .then(data => {
          if (data.message === 'Login successful!') {
            localStorage.setItem('professionalId', data.professional_id);
            localStorage.setItem('isAuthenticated', 'true');
            localStorage.setItem('role', 'ServiceProfessional');
            localStorage.setItem('jwtToken',data.access_token)
            this.message = data.message;
            this.isError = false;
            setTimeout(() => {
              window.location.href = '/serviceprofessional_dashboard';
            }, 2000);
          } else {
            this.message = data.message;
            this.isError = data.message !== "You are blocked. Please contact admin";
          }
        })
        .catch(error => {
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

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 10px;
  border: 1px solid #f5c6cb;
  border-radius: 5px;
  margin-top: 10px;
}

.success-message {
  background-color: #d4edda;
  color: #155724;
  padding: 10px;
  border: 1px solid #c3e6cb;
  border-radius: 5px;
  margin-top: 10px;
}
</style>