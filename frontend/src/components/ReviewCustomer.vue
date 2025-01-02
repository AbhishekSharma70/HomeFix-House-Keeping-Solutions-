<template>
    <nav class="navbar navbar-expand-lg mb-4 shadow-sm bg-primary text-white fixed-top">
      <div class="container-fluid">
        <a class="navbar-brand text-white" @click="goToAdminDashboard">HomeFix | Block Management</a>
      </div>
    </nav>
    <br>
    <br>
    <div class="container" style="margin-top:70px">
        <br>
        <br>
      <h2>Reviews for Professional ID: {{ professionalId }}</h2>
      <br>
      <br>
      <table class="table table-hover table-striped">
        <thead>
          <tr>
            <th>Type</th>
            <th>Professional ID</th>
            <th>Rate Customer</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="review in reviews" :key="review.customer_id">
            <td>{{ review.type }}</td>
            <td>{{ review.professional_id }}</td>
            <td>{{ review.View }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        reviews: [],
        customerId: this.$route.params.id,
      };
    },
    mounted() {
      this.fetchReviews();
    },
    methods: {
      fetchReviews() {
        fetch(`http://localhost:8000/api/customer/${this.customerId}/reviews`, {
          headers: {
            'Content-Type': 'application/json',
          },
        })
        .then(response => response.json())
        .then(data => {
          this.reviews = data.reviews;
        })
        .catch(error => console.error('Error fetching reviews:', error));
      },
      goToAdminDashboard(){
        this.$router.push({'name':'AdminDashboard'})
      }
    }
  };
  </script>