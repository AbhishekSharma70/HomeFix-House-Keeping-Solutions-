<template>
  <nav class="navbar navbar-expand-lg bg-primary text-white">
    <div class="container-fluid">
      <a class="navbar-brand text-white" @click="goToCustomerDashboard">HomeFix | Close Service Requests</a>
    </div>
    <div class="d-flex justify-content-end">
      <button @click="logout" class="btn btn-danger mx-2">Logout</button>
    </div>
  </nav>

  <div class="container d-flex justify-content-center mt-5">
    <div class="card shadow-lg p-4 w-50" style="background-color: #f7fafc">
      <h3 class="text-center text-primary mb-4">Close Service Request</h3>

      <form @submit.prevent="submitCloseRequest">
        <div class="form-group mb-4">
          <label for="dateOfCompletion" class="form-label">Date of Completion</label>
          <input type="date" v-model="dateOfCompletion" class="form-control" id="dateOfCompletion" required />
        </div>

        <div class="form-group mb-4">
          <label for="remarks" class="form-label">Remarks</label>
          <textarea id="remarks" v-model="remarks" class="form-control" rows="3" placeholder="Enter your remarks here" required></textarea>
        </div>

        <div class="form-group mb-4">
          <label for="rating" class="form-label">Rating (1 to 5)</label>
          <input type="number" id="rating" v-model="rating" class="form-control" min="1" max="5" required />
        </div>

        <div class="form-group mb-4">
          <label for="amount" class="form-label">Amount</label>
          <input type="number" v-model="amount" class="form-control" id="amount" disabled />
        </div>

        <div class="d-grid gap-2">
          <button type="submit" class="btn btn-primary">Submit</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      dateOfCompletion: '',
      remarks: '',
      rating: 1,
      amount: 0,
      requestId: this.$route.params.requestId,
    };
  },
  created() {
    this.fetchServiceRequest();
  },
  methods: {
    async fetchServiceRequest() {
      try {
        const response = await fetch(`http://localhost:8000/api/service_requests/${this.requestId}`);
        const data = await response.json();
        this.amount = data.amount;
      } catch (error) {
        console.error('Error fetching service request details:', error);
      }
    },
    async submitCloseRequest() {
      try {
        const response = await fetch(`http://localhost:8000/api/service_requests/${this.requestId}/close`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            dateOfCompletion: this.dateOfCompletion,
            remarks: this.remarks,
            rating: this.rating,
          }),
        });

        if (response.ok) {
          alert('Service request closed successfully!');
          this.$router.push({ name: 'CustomerDashboard' });
        } else {
          alert('Failed to close service request');
        }
      } catch (error) {
        console.error('Error closing request:', error);
      }
    },
    goToCustomerDashboard() {
      this.$router.push({ name: 'CustomerDashboard' });
    },
    logout() {
      localStorage.removeItem('customerId');
      this.$router.push({ name: 'IndexFirst' });
    }
  }
};
</script>

<style scoped>
.card {
  max-width: 500px;
}
textarea {
  resize: none;
}
</style>