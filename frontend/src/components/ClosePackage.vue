<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary mb-0">
    <div class="container-fluid">
      <a class="navbar-brand text-white" @click="goToCustomerDashboard">HomeFix | Close Service Package</a>
    </div>
    <div class="d-flex justify-content-between mb-4">
      <button @click="logout" class="btn btn-danger mx-1">Logout</button>
    </div>
  </nav>
  
  <div class="container mt-5">
    <div class="card shadow-sm p-4 bg-custom-card">
      <h2 class="text-center text-primary mb-4">Close Service Package</h2>

      <form @submit.prevent="submitCloseRequest">
        <div class="mb-3">
          <label for="dateOfCompletion" class="form-label">Date of Completion</label>
          <input type="date" v-model="dateOfCompletion" class="form-control" required />
        </div>

        <div class="mb-3">
          <label for="remarks" class="form-label">Remarks</label>
          <textarea
            id="remarks"
            v-model="remarks"
            class="form-control"
            rows="3"
            placeholder="Provide your feedback"
            required
          ></textarea>
        </div>

        <div class="mb-3">
          <label for="rating" class="form-label">Rating</label>
          <input
            type="number"
            id="rating"
            v-model="rating"
            class="form-control"
            min="1"
            max="5"
            placeholder="Rate between 1 and 5"
            required
          />
        </div>

        <button type="submit" class="btn btn-primary w-100">Submit</button>
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
    };
  },
  methods: {
    async submitCloseRequest() {
      const packageId = this.$route.params.pkgId;
      try {
        const response = await fetch(`http://localhost:8000/api/booked_service_packages/${packageId}/close`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            dateOfCompletion: this.dateOfCompletion,
            remarks: this.remarks,
            rating: this.rating,
          }),
        });

        if (response.ok) {
          alert('Service package closed successfully!');
          this.$router.push({ name: 'CustomerDashboard' });
        } else {
          const data = await response.json();
          alert(data.error || 'Failed to close the service package.');
        }
      } catch (error) {
        console.error('Error closing the package:', error);
      }
    },
    goToCustomerDashboard() {
      this.$router.push({ name: 'CustomerDashboard' });
    },
    logout() {
      localStorage.removeItem('customerId');
      this.$router.push({ name: 'IndexFirst' });
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: auto;
}

.navbar {
  background-color: #00796b;
}

.navbar-brand {
  font-weight: bold;
  font-size: 1.2rem;
  cursor: pointer;
}

.btn-danger {
  font-size: 0.9rem;
}

.card {
  border-radius: 8px;
  padding: 20px;
}

.bg-custom-card {
  background-color: #e0f7fa;
}

.text-center {
  text-align: center;
}

.form-label {
  font-weight: 600;
}

.form-control {
  border-radius: 5px;
}

.btn-primary {
  background-color: #00796b;
  border-color: #00796b;
  font-weight: bold;
}
</style>