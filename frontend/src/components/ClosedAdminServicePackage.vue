<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary mb-0">
    <div class="container-fluid">
      <a class="navbar-brand text-white" @click="goToCustomerDashboard">HomeFix | Close HomeFix Packages</a>
    </div>
    <div class="d-flex justify-content-end">
      <button @click="logout" class="btn btn-danger mx-1">Logout</button>
    </div>
  </nav>

  <div class="container mt-5">
    <div class="card shadow-sm p-4 form-container">
      <h2 class="text-center text-primary mb-4">Close HomeFix Package</h2>
      <form @submit.prevent="submitClosure">
        <div class="mb-3">
          <label for="completionDate" class="form-label">Date of Completion</label>
          <input type="date" v-model="completionDate" class="form-control" id="completionDate" required />
        </div>
        <div class="mb-3">
          <label for="remarks" class="form-label">Remarks</label>
          <textarea v-model="remarks" class="form-control" id="remarks" rows="3" required></textarea>
        </div>
        <div class="mb-3">
          <label for="rating" class="form-label">Rating</label>
          <input type="number" v-model="rating" min="1" max="5" class="form-control" id="rating" required />
        </div>
        <button type="submit" class="btn btn-success w-100 mt-3">Submit</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      completionDate: '',
      remarks: '',
      rating: '',
    };
  },
  methods: {
    async submitClosure() {
      const pkgId = this.$route.params.pkgId;
      try {
        const response = await fetch(`http://localhost:8000/api/close_package/${pkgId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            completion_date: this.completionDate,
            remarks: this.remarks,
            rating: this.rating,
          }),
        });

        if (response.ok) {
          alert('Package closed successfully.');
          this.$router.push({ name: 'CustomerDashboard' });
        } else {
          const error = await response.json();
          console.error('Error closing package:', error);
        }
      } catch (error) {
        console.error('Error submitting closure:', error);
      }
    },
    goToCustomerDashboard() {
      this.$router.push({ name: 'CustomerDashboard' });
    },
  },
};
</script>

<style scoped>
body {
  background-color: #f4f6f9;
}
.navbar {
  background-color: #00796b;
  color: white;
}
.navbar-brand {
  font-weight: bold;
  font-size: 1.25rem;
  color: white;
}
.container {
  max-width: 600px;
}
.card {
  border-radius: 8px;
}
.form-container {
  background-color: #e0f7fa;
  border: 1px solid #b2ebf2;
}
.form-label {
  font-weight: bold;
}
.form-control {
  border: 1px solid #b2ebf2;
  border-radius: 4px;
  padding: 10px;
}
textarea.form-control {
  resize: none;
}
.btn-success {
  background-color: #00796b;
  border: none;
  transition: background-color 0.3s;
}
.btn-success:hover {
  background-color: #004d40;
}
.btn-danger {
  background-color: #d32f2f;
  border: none;
  transition: background-color 0.3s;
}
.btn-danger:hover {
  background-color: #b71c1c;
}
</style>