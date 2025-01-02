<template>
  <div class="approval-page">
    <nav class="navbar navbar-expand-lg mb-4 shadow-sm bg-primary text-white fixed-top">
      <div class="container-fluid">
        <a class="navbar-brand text-white" @click="goToAdminDashboard">HomeFix | Service Professional Approval</a>
      </div>
    </nav>

    <div class="container" style="margin-top:70px;">
      <h1 class="text-center mb-4">Pending Service Professional Approvals</h1>
      <table class="table table-hover table-striped">
        <thead class="thead-light">
          <tr>
            <th>ID</th>
            <th>Full Name</th>
            <th>Service Type</th>
            <th>Address</th>
            <th>Pincode</th>
            <th>Document</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="professional in pendingProfessionals" :key="professional.id">
            <td>{{ professional.id }}</td>
            <td>{{ professional.full_name }}</td>
            <td>{{ professional.service_type }}</td>
            <td>{{ professional.address }}</td>
            <td>{{ professional.pincode }}</td>
            <td>
              <a :href="`http://localhost:8000/static/documents/${professional.document}`" target="_blank" class="btn btn-link">
                View Document
              </a>
            </td>
            <td>
              <button class="btn btn-success" @click="approveProfessional(professional.id)">Approve</button>
              <button class="btn btn-danger" @click="rejectProfessional(professional.id)">Reject</button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="message" :class="['message', isError ? 'error-message' : 'success-message']">
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      pendingProfessionals: [],
      message: '',
      isError: false,
    };
  },
  methods: {
    fetchPendingProfessionals() {
      const token=localStorage.getItem('jwtToken')
      if(!token){
        alert('You are not logged in,Redirecting you to the login page')
        this.$router.push({'name':'AdminLogin'})
        return;
      }
      fetch('http://localhost:8000/api/pending_professionals',{
        headers:{
          'Content-Type':'application/json',
          'Authorization':`Bearer ${token}`
        }
      })
        .then(response => response.json())
        .then(data => {
          this.pendingProfessionals = data.professionals;
        })
        .catch(error => {
          this.message = 'Error fetching data: ' + error.message;
          this.isError = true;
        });
    },
    approveProfessional(id) {
      const token=localStorage.getItem('jwtToken')
      if(!token){
        alert('You are not logged in,Redirecting you to the login page.')
        this.$router.push({'name':'AdminLogin'})
        return;
      }
      fetch(`http://localhost:8000/api/approve_professional/${id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization':`Bearer ${token}`
        },
        body: JSON.stringify({})  // Empty body as it's a POST request
      })
        .then(response => response.json())
        .then(data => {
          this.message = data.message;
          this.isError = false;
          this.fetchPendingProfessionals();  // Refresh the list after approval
        })
        .catch(error => {
          this.message = 'Error: ' + error.message;
          this.isError = true;
        });
    },
    rejectProfessional(id) {
      const token=localStorage.getItem('jwtToken')
      if(!token){
        alert('You are not logged in,Redirecting you to the login page.')
        this.$router.push({'name':'AdminLogin'})
        return;
      }
      fetch(`http://localhost:8000/api/reject_professional/${id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization':`Bearer ${token}`
        },
        body: JSON.stringify({})  // Empty body as it's a POST request
      })
        .then(response => response.json())
        .then(data => {
          this.message = data.message;
          this.isError = false;
          this.fetchPendingProfessionals();  // Refresh the list after rejection
        })
        .catch(error => {
          this.message = 'Error: ' + error.message;
          this.isError = true;
        });
    },
    goToAdminDashboard(){
      this.$router.push({name:'AdminDashboard'})
    }
  },
  mounted() {
    this.fetchPendingProfessionals();
  }
};
</script>

<style scoped>
/* Page Container */
.approval-page {
  background-color: #f9f9f9;
  padding: 20px;
  min-height: 100vh;
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

/* Table Styling */
.table {
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.table th,
.table td {
  vertical-align: middle;
}

/* Hover Effect for Rows */
.table-hover tbody tr:hover {
  background-color: #e9f7fa; /* Light blue on hover */
}

/* Message Styles */
.message {
  margin-top: 20px;
  padding: 10px;
  border-radius: 5px;
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

/* Button Styles */
.btn-link {
  color: #007bff;
  text-decoration: none;
}

.btn-link:hover {
  text-decoration: underline;
}
</style>