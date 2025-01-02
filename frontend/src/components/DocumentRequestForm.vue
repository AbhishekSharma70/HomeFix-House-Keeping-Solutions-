<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary mb-0">
    <div class="container-fluid">
      <a class="navbar-brand text-white" @click="goToCustomerDashboard">HomeFix | Documents</a>
    </div>
  </nav>
  <br>
  <br>
  <br>
  <br>
  <div class="container-fluid d-flex justify-content-center align-items-center" style="margin-top: 50px;" id="app">
    <div class="card p-4 form-card shadow-lg">
      <div class="card-body text-center">
        <h2 class="form-title">Your Activity Report</h2>
        <form @submit.prevent="sendReport" class="activity-form">
          <div class="form-group mb-4">
            <label for="date" class="form-label">Enter Date:</label>
            <input type="date" v-model="date" class="form-control" required />
          </div>
          <div class="form-group mb-4">
            <label for="email" class="form-label">Enter Email:</label>
            <input type="email" v-model="email" class="form-control" required />
          </div>
          <button type="submit" class="btn btn-primary form-submit-btn">Submit</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      date: '',
      email: ''
    };
  },
  methods: {
    logout(){
      localStorage.removeItem('customerId');
      localStorage.removeItem('jwtToken')
      this.$router.push({ name: 'IndexFirst' });
    },
    sendReport() {
      const token=localStorage.getItem('jwtToken')
      if(!token){
        alert('You are not logged in. Redirecting to login page')
        this.$router.push({'name':'CustomerLogin'})
        return;
      }
      const customer_id = localStorage.getItem('customerId');
      if (!customer_id || !this.date || !this.email) {
        alert('Please fill out all fields');
        return;
      }

      fetch('http://localhost:8000/api/request_activity_report', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization':`Bearer ${token}`
        },
        body: JSON.stringify({
          date: this.date,
          customer_id: customer_id,
          email: this.email
        }),
      })
      .then(response => response.json())
      .then(data => {
        if (data.message) {
          alert(data.message);
        } else {
          alert('Failed to send report');
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
    },
    goToCustomerDashboard() {
      this.$router.push({ name: 'CustomerDashboard' });
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

.form-card {
  background-color: #e0f7fa;
  max-width: 400px;
  width: 100%;
  border-radius: 12px;
}

.form-title {
  color: #00796b;
  font-weight: 700;
}

.activity-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  position: relative;
}

.form-label {
  font-weight: 500;
  color: #00796b;
  font-size: 14px;
}

.form-control {
  border: none;
  border-bottom: 2px solid #00796b;
  border-radius: 0;
  box-shadow: none;
  padding: 10px;
  transition: border-color 0.3s;
}

.form-control:focus {
  border-color: #004d40;
  box-shadow: none;
}

.form-submit-btn {
  background-color: #00796b;
  border: none;
  color: white;
  padding: 10px;
  border-radius: 6px;
  font-weight: 600;
  transition: background-color 0.3s;
}

.form-submit-btn:hover {
  background-color: #004d40;
  color: white;
}
</style>