<template>

<nav class="navbar navbar-expand-lg bg-body-tertiary mb-0">
    <div class="container-fluid">
        <a class="navbar-brand text-white" @click="goToCustomerDashboard">HomeFix | HomeFix Packages</a>
    </div>
</nav>

    <div class="container mt-5">
      <h2 class="text-center">Requested Service Requests</h2>
      <br>
      <br>
      <table class="table ">
        <thead>
          <tr>
            <th>Request ID</th>
            <th>Customer ID</th>
            <th>Professional ID</th>
            <th>Date of Request</th>
            <th>Description</th>
            <th>Price</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in serviceRequests" :key="request.id">
            <td>{{ request.id }}</td>
            <td>{{ request.customer_id }}</td>
            <td>{{ request.professional_id }}</td>
            <td>{{ request.date_of_request }}</td>
            <td>{{ request.description }}</td>
            <td>{{ request.price }}</td>
            <td>
              <button @click="openUpdateModal(request)" class="btn btn-primary">Update</button>
            </td>
          </tr>
        </tbody>
      </table>
  
      <!-- Update Modal -->
      <div v-if="selectedRequest" class="modal" tabindex="-1" role="dialog" style="display: block;">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Update Service Request {{ selectedRequest.id }}</h5>
            </div>
            <div class="modal-body">
             <div class="form-group">
                <label>Date of Request: </label>
                <input type="date" v-model="selectedRequest.date_of_request" class="form-control" />
              </div>  
              <div class="form-group">
                <label>Description</label>
                <input v-model="selectedRequest.description" class="form-control" />
              </div>
              <div class="form-group">
                <label>Price</label>
                <input type="number" v-model="selectedRequest.price" class="form-control" />
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-primary" @click="updateServiceRequest">Save changes</button>
              <button type="button" class="btn btn-secondary" @click="closeUpdateModal">Close</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        serviceRequests: [],
        selectedRequest: null,
      };
    },
    created() {
      this.fetchServiceRequests();
    },
    methods: {
      async fetchServiceRequests() {
        const token=localStorage.getItem('jwtToken')
        if(!token){
          alert('You are not logged in,Redirecting you to the login page')
          this.$router.push({'name':'CustomerLogin'})
          return
        }
        try {
          const response = await fetch('http://localhost:8000/api/service_requests/requested',{
            headers:{
                'Content-Type':'application/json',
                'Authorization':`Bearer ${token}`
            }
          });
          const data = await response.json();
          this.serviceRequests = data.service_requests;
        } catch (error) {
          console.error("Error fetching service requests:", error);
        }
      },
      openUpdateModal(request) {
        this.selectedRequest = { ...request }; // Make a copy for editing
      },
      closeUpdateModal() {
        this.selectedRequest = null;
      },
      async updateServiceRequest() {
        const token=localStorage.getItem('jwtToken')
        if(!token){
          alert('You are not logged in,Redirecting you to the login page')
          this.$router.push({'name':'CustomerLogin'})
          return
        }
        const requestId = this.selectedRequest.id;
        try {
          const response = await fetch(`http://localhost:8000/api/service_requests/${requestId}/update`, {
            method: "PUT",
            headers: { "Content-Type": "application/json",
                'Authorization':`Bearer ${token}`
             },
            body: JSON.stringify(this.selectedRequest),
          });
          if (response.ok) {
            alert("Service request updated successfully!");
            this.closeUpdateModal();
            this.fetchServiceRequests(); // Refresh the list
          } else {
            alert("Failed to update service request.");
          }
        } catch (error) {
          console.error("Error updating service request:", error);
        }
      },
      goToCustomerDashboard(){
        this.$router.push({'name':'CustomerDashboard'})
      }
    },
  };
  </script>
  
  <style>
  .modal {
    display: none;
    background: rgba(0, 0, 0, 0.6);
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 1000;
  }
  .modal-dialog {
    max-width: 500px;
    margin: 50px auto;
  }
  </style>