<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary mb-0">
      <div class="container-fluid">
        <a class="navbar-brand" @click="goToIndex">HomeFix | HomeFix Packages</a>
      </div>
    </nav>
  
    <div class="about-container">
      <section class="hero-section">
        <h1>Welcome to Our Household Services App</h1>
        <p>
          Connect with skilled professionals for home services, from plumbing to painting.
          Discover more about our offerings below.
        </p>
      </section>
  
      <section class="data-summary">
        <h2>Service Overview</h2>
        <div class="card-container">
          <div class="card" v-if="aboutData.service_professionals">
            <h3>Service Professionals by Type</h3>
            <ul>
              <li v-for="(count, type) in aboutData.service_professionals" :key="type">
                {{ type }}: {{ count }}
              </li>
            </ul>
          </div>
  
          <div class="card" v-if="aboutData.service_requests">
            <h3>Service Requests by Type</h3>
            <ul>
              <li v-for="(count, type) in aboutData.service_requests" :key="type">
                {{ type }}: {{ count }}
              </li>
            </ul>
          </div>
  
          <div class="card" v-if="aboutData.service_packages">
            <h3>Service Packages by Type</h3>
            <ul>
              <li v-for="(count, type) in aboutData.service_packages" :key="type">
                {{ type }}: {{ count }}
              </li>
            </ul>
          </div>
  
          <div class="card" v-if="aboutData.homefix_packages">
            <h3>Homefix Packages by Type</h3>
            <ul>
              <li v-for="(count, type) in aboutData.homefix_packages" :key="type">
                {{ type }}: {{ count }}
              </li>
            </ul>
          </div>
        </div>
      </section>
    </div>
  </template>
  
  <script>
  export default {
    name: 'AboutPage',
    data() {
      return {
        aboutData: {}
      };
    },
    created() {
      this.fetchAboutData();
    },
    methods: {
      async fetchAboutData() {
        try {
          const response = await fetch('http://localhost:8000/api/about');
          if (!response.ok) throw new Error("Failed to fetch about data");
          const data = await response.json();
          this.aboutData = data.data_summary;
        } catch (error) {
          console.error("Error fetching about data:", error);
        }
      },
      goToIndex(){
        this.$router.push({ name: 'IndexFirst' });
      }
    }
  };
  </script>
  
  <style scoped>
  * {
    box-sizing: border-box;
  }
  
  .about-container {
    font-family: 'Roboto', sans-serif;
    color: #333;
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .navbar-brand {
    font-size: 1.5rem;
    color: #f1f1f1;
    cursor: pointer;
  }
  
  .hero-section {
    text-align: center;
    margin-bottom: 40px;
    padding: 40px;
    background: linear-gradient(135deg, #63dbff, #478ca3);
    color: #ffffff;
    border-radius: 10px;
  }
  
  .hero-section h1 {
    font-size: 3rem;
    margin-bottom: 15px;
  }
  
  .hero-section p {
    font-size: 1.2rem;
    margin-bottom: 20px;
  }
  
  .cta-button {
    background-color: #4a47a3;
    color: #ffffff;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    font-size: 1rem;
    cursor: pointer;
    transition: background 0.3s;
  }
  
  .cta-button:hover {
    background-color: #6c63ff;
  }
  
  .data-summary h2 {
    font-size: 2.2rem;
    color: #4a47a3;
    margin-bottom: 20px;
    text-align: center;
  }
  
  .card-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
  }
  
  .card {
    flex: 1 1 calc(45% - 20px);
    background-color: #ffffff;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s, box-shadow 0.3s;
  }
  
  .card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 15px rgba(0, 0, 0, 0.15);
  }
  
  .card h3 {
    font-size: 1.6rem;
    color: #4781a3;
    margin-bottom: 10px;
  }
  
  .card ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  
  .card li {
    font-size: 1.1rem;
    color: #34495e;
    padding: 5px 0;
  }
  
  @media (max-width: 768px) {
    .card-container {
      flex-direction: column;
    }
  
    .hero-section h1 {
      font-size: 2.5rem;
    }
  }
  </style>