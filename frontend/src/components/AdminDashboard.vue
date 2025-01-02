<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light shadow-sm">
    <div class="container-fluid">
      <a class="navbar-brand fw-bold text-white" href="#">HomeFix | Admin Dashboard</a>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <button @click="goToHomeFixPackages" class="btn btn-primary mx-1">HomeFix Packages</button>
          </li>
          <li class="nav-item">
            <button @click="gotoAdminServicePackage" class="btn btn-secondary mx-1">Create a Package</button>
          </li>
          <li class="nav-item">
            <button type="button" @click="goToDocuments" class="btn btn-info mx-1">Documents</button>
          </li>
          <li class="nav-item">
            <router-link to="/admin/professional-approvals">
              <button class="btn btn-success mx-1">Approvals</button>
            </router-link>
          </li>
          <li class="nav-item">
            <button @click="$router.push('/admin/blocks')" class="btn btn-primary mx-1">Blocks</button>
          </li>
          <li class="nav-item">
            <button @click="logout" class="btn btn-danger mx-1">Logout</button>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  
    <!-- Row 1: Pie Chart for Customers vs Professionals -->
    <div class="card-group">
    <div class="chart-container">
      <h3 class="text-center mb-4">Number of Customers vs Service Professionals</h3>
      <canvas id="customerProfessionalPieChart"></canvas>
    </div>

    <div class="chart-container">
      <h3 class="text-center my-4">Blocked vs Unblocked Users</h3>
      <canvas id="blockedUnblockedBarChart"></canvas>
    </div>

    <div class="chart-container">
      <h3 class="text-center my-4">Number of Service Professionals by Type</h3>
      <canvas id="serviceProfessionalChart"></canvas>
    </div>
    </div>

    <div class="card-group">
    <div class="chart-container">
      <h3 class="text-center my-4">Number of Service Requests by Type</h3>
      <canvas id="serviceRequestChart"></canvas>
    </div>

    <div class="chart-container">
      <h3 class="text-center my-4">Number of Service Packages by Type</h3>
      <canvas id="servicePackagesChart"></canvas>
     </div>

   <div class="chart-container">
     <h3 class="text-center my-4">Number of HomeFix Packages by Type</h3>
     <canvas id="homeFixPackagesChart"></canvas>
    </div>
    </div>
    
</template>

<script>
import { Chart, PieController, BarController, CategoryScale, LinearScale, ArcElement, BarElement, Legend, Tooltip, Title } from 'chart.js';

// Register the required controllers, elements, scales, and plugins
Chart.register(PieController, BarController, CategoryScale, LinearScale, ArcElement, BarElement, Legend, Tooltip, Title);

export default {
  mounted(){
      this.getCustomerServiceProfessionalCount();
      this.getBlockedUnblockedUsers();
      this.getServiceProfessionalsByType();
      this.getServiceRequestsByType();
      this.getServicePackagesByType();
      this.getHomeFixPackagesByType();
    },
  methods: {
    logout(){
      localStorage.removeItem('adminId');
      localStorage.removeItem('jwtToken');
      this.$router.push({ name: 'IndexFirst' });
    },
    getCustomerServiceProfessionalCount() {
      fetch('http://localhost:8000/api/customer_service_professional_count')
        .then(response => response.json())
        .then(data => {
          const ctx = document.getElementById('customerProfessionalPieChart').getContext('2d');
          new Chart(ctx, {
            type: 'pie',
            data: {
              labels: ['Customers', 'Service Professionals'],
              datasets: [{
                data: [data.customers, data.professionals],
                backgroundColor: ['#36A2EB', '#FF6384']
              }]
            }
          });
        });
    },    
    // Stacked Bar Chart: Blocked vs Unblocked Users
    getBlockedUnblockedUsers() {
      fetch('http://localhost:8000/api/blocked_unblocked_users')
        .then(response => response.json())
        .then(data => {
          const ctx = document.getElementById('blockedUnblockedBarChart').getContext('2d');
          new Chart(ctx, {
            type: 'bar',
            data: {
              labels: ['Customers', 'Service Professionals'],
              datasets: [
                {
                  label: 'Blocked',
                  data: [data.blocked_customers, data.blocked_professionals],
                  backgroundColor: '#FF6384'
                },
                {
                  label: 'Unblocked',
                  data: [data.unblocked_customers, data.unblocked_professionals],
                  backgroundColor: '#36A2EB'
                }
              ]
            },
            options: {
              scales: {
                x: { stacked: true },
                y: { stacked: true,
                  ticks:{
                    stepSize:1
                  }
                 }
              }
            }
          });
        });
    },

    getServiceProfessionalsByType() {
      fetch('http://localhost:8000/api/service_professionals_by_type')
        .then(response => response.json())
        .then(data => {
          const ctx = document.getElementById('serviceProfessionalChart').getContext('2d');
          new Chart(ctx, {
            type: 'bar',
            data: {
              labels: Object.keys(data), // ['Carpenter', 'Plumber', etc.]
              datasets: [{
                label: 'Number of Service Professionals',
                data: Object.values(data), // [10, 5, etc.]
                backgroundColor: '#36A2EB'
              }]
            },
            options: {
              scales: {
                x: { title: { display: true, text: 'Service Type' } },
                y: { title: { display: true, text: 'Count' }, beginAtZero: true,
                   ticks:{
                    stepSize:1
                   } }
              }
            }
          });
        });
    },

    // Fetch and display service requests by type
    getServiceRequestsByType() {
      fetch('http://localhost:8000/api/service_requests_by_type')
        .then(response => response.json())
        .then(data => {
          const ctx = document.getElementById('serviceRequestChart').getContext('2d');
          new Chart(ctx, {
            type: 'bar',
            data: {
              labels: Object.keys(data), // ['Carpenter', 'Plumber', etc.]
              datasets: [{
                label: 'Number of Service Requests',
                data: Object.values(data), // [20, 15, etc.]
                backgroundColor: '#FF6384'
              }]
            },
            options: {
              scales: {
                x: { title: { display: true, text: 'Service Type' } },
                y: { title: { display: true, text: 'Count' }, beginAtZero: true, 
                ticks:{
                  stepSize:1
                } }
              }
            }
          });
        });
    },
    goToDocuments(){
      this.$router.push({'name':'DocumentAdminPage'})
    },
    gotoAdminServicePackage(){
      this.$router.push({'name':'AdminServicePackage'})
    },
    goToHomeFixPackages(){
      this.$router.push({'name':'AdminHomeFixPackage'})
    },
    getServicePackagesByType() {
      fetch('http://localhost:8000/api/service_packages_by_type')
        .then(response => response.json())
        .then(data => {
          const ctx = document.getElementById('servicePackagesChart').getContext('2d');
          new Chart(ctx, {
            type: 'bar',
            data: {
              labels: Object.keys(data), // e.g., ['Carpenter', 'Plumber', etc.]
              datasets: [{
                label: 'Number of Service Packages',
                data: Object.values(data), // e.g., [15, 20, etc.]
                backgroundColor: '#4BC0C0'
              }]
            },
            options: {
              scales: {
                x: { title: { display: true, text: 'Service Type' } },
                y: { title: { display: true, text: 'Count' }, beginAtZero: true,
                   ticks:{
                    stepSize:1
                  } }
              }
            }
          });
        });
    },

    getHomeFixPackagesByType() {
      fetch('http://localhost:8000/api/homefix_packages_by_type')
        .then(response => response.json())
        .then(data => {
          const ctx = document.getElementById('homeFixPackagesChart').getContext('2d');
          new Chart(ctx, {
            type: 'bar',
            data: {
              labels: Object.keys(data),
              datasets: [{
                label: 'Number of HomeFix Packages',
                data: Object.values(data),
                backgroundColor: '#FFCE56'
              }]
            },
            options: {
              scales: {
                x: { title: { display: true, text: 'Service Type' } },
                y: { title: { display: true, text: 'Count' }, beginAtZero: true,
                  ticks:{
                    stepSize:1
                  } }
              }
            }
          });
        });
    },

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
  font-size: 1.5rem;
}

.chart-container {
  max-width: 400px; /* Decreased from 700px */
  margin: 2rem auto;
  padding: 1rem; /* Added padding for better spacing */
  border: 1px solid #ddd; /* Optional: Add border for better visibility */
  border-radius: 8px; /* Optional: Add border radius for rounded corners */
  background-color: #f8f9fa; /* Optional: Light background color */
}

.container h3 {
  font-weight: 600;
  color: #333;
}

.btn {
  padding: 0.6rem 1.5rem; /* Increased padding for better touch targets */
  font-weight: 500;
  border-radius: 10px; /* Slightly increased border radius */
  transition: background-color 0.3s, color 0.3s;
  font-size: 1rem; /* Increased font size */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Added shadow for depth */
}

.btn-outline-primary, .btn-outline-secondary, .btn-outline-info, .btn-outline-success, .btn-outline-danger {
  border-width: 2px; /* Slightly thicker borders */
}

.btn-outline-primary {
  background-color: #007bff; /* Base color */
  color: white;
}

.btn-outline-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-outline-info {
  background-color: #17a2b8;
  color: white;
}

.btn-outline-success {
  background-color: #28a745;
  color: white;
}

.btn-outline-danger {
  background-color: #dc3545;
  color: white;
}

.btn-outline-primary:hover, .btn-outline-secondary:hover, .btn-outline-info:hover, .btn-outline-success:hover, .btn-outline-danger:hover {
  filter: brightness(90%); /* Slightly darken on hover */
}
</style>