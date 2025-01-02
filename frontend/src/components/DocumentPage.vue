<template>
  <div class="documents-page">
    <nav class="navbar navbar-expand-lg mb-4 shadow-sm bg-primary text-white">
      <div class="container-fluid">
        <a class="navbar-brand text-white" @click="goToAdminDashboard">HomeFix | Documents</a>
        <div class="d-flex">
          <button @click="logout" class="btn btn-danger">Logout</button>
        </div>
      </div>
    </nav>

    <div class="container d-flex justify-content-center align-items-center" style="height: calc(100vh - 64px);">
      <div class="card shadow-lg p-4" style="background-color: #e0f7fa; max-width: 400px; width: 100%;">
        <div class="card-body">
          <h2 class="text-center mb-4">Request Service Report</h2>
          <form @submit.prevent="submitRequest">
            <div class="mb-3">
              <label for="endDate" class="form-label">Date</label>
              <input type="date" v-model="endDate" class="form-control" required />
            </div>
            <div class="mb-3">
              <label for="email" class="form-label">Email Address</label>
              <input type="email" v-model="email" class="form-control" required />
            </div>
            <button type="submit" class="btn btn-primary w-100">Submit</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      endDate: '',
      email: ''
    };
  },
  methods: {
    async submitRequest() {
      // Validate form fields before sending the request

      const token=localStorage.getItem('jwtToken')
      if(!token){
        alert('You are not logged in,Redirecting you to the login page')
        this.$router.push({'name':'AdminLogin'})
        return;
      }


      if (!this.endDate || !this.email) {
        alert('Please fill out all fields.');
        return;
      }

      try {
        const response = await fetch('http://localhost:8000/api/send_report_email', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization':`Bearer ${token}`
          },
          body: JSON.stringify({
            end_date: this.endDate,
            email: this.email
          }),
        });

        if (response.ok) {
          alert('Report request submitted successfully! Check your email shortly.');
        } else {
          const errorData = await response.json();
          alert(`Failed to submit report request: ${errorData.message}`);
        }
      } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while submitting the report request.');
      }
    },
    goToAdminDashboard() {
      this.$router.push({ name: 'AdminDashboard' });
    },
    logout() {
      localStorage.removeItem('adminId');
      localStorage.removeItem('jwtToken')
      this.$router.push({ name: 'AdminLogin' });
    }
  }
};
</script>

<style scoped>
/* Container Styling */
.container {
  max-width: 700px;
}

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

/* Card Styling */
.card {
  border-radius: 1rem;
  transition: box-shadow 0.3s ease;
  border: 1px solid #e0e0e0; /* Add border */
}

.card:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); /* Enhanced shadow on hover */
}

/* Title Styling */
.card h2 {
  color: #333; /* Darker title color */
}

/* Form Label Styling */
.form-label {
  font-weight: bold;
  color: #555; /* Slightly darker color for better contrast */
}

/* Input Field Styling */
.form-control {
  border-radius: 0.5rem;
  border: 1px solid #007bff; /* Primary color for borders */
  transition: border-color 0.3s ease;
}

.form-control:focus {
  border-color: #0056b3; /* Darker primary color on focus */
  box-shadow: 0 0 5px rgba(0, 86, 179, 0.5); /* Add shadow on focus */
}

/* Button Styling */
.btn {
  font-weight: 500;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.btn-primary:hover {
  background-color: #0056b3; /* Darker color on hover */
  border-color: #0056b3;
  transform: translateY(-2px);
}
</style>