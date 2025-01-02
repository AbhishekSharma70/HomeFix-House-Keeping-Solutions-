import { createRouter, createWebHistory } from 'vue-router';
import AdminSignup from '../components/AdminSignup.vue';
import AdminLogin from '../components/AdminLogin.vue';
import CustomerLogin from '../components/CustomerLogin.vue';
import CustomerSignup from '../components/CustomerSignup.vue';
import ServiceProfessionalLogin from '../components/ServiceProfessionalLogin.vue';
import ServiceProfessionalSignup from '../components/ServiceProfessionalSignup.vue';
import IndexFirst from '../components/IndexFirst.vue';
import CustomerDashboard from '../components/CustomerDashboard.vue';
import ServiceRequest from '../components/ServiceRequest.vue';
import ProfessionalProfile from '../components/ProfessionalProfile.vue'
import ServiceProfessionalDashboard from '../components/ServiceProfessionalDashboard.vue'
import CloseServiceRequest from '../components/CloseServiceRequest.vue'
import CreateServicePackage from '../components/CreateServicePackage.vue'
import ShowCustomerPackage from '../components/ShowCustomerPackage.vue'
import ClosePackage from '../components/ClosePackage.vue'
import EditServiceRequest from '../components/EditServiceRequest.vue'
import AdminDashboard from '../components/AdminDashboard.vue'
import BlockManagement from '../components/BlockManagement.vue'
import ProfessionalApprovals from '../components/ProfessionalApprovals.vue'
import DocumentRequestForm from '@/components/DocumentRequestForm.vue';
import DocumentPage from '@/components/DocumentPage.vue';
import AdminServicePackage from '@/components/AdminServicePackage.vue';
import ProfessionalProfileAdmin from '@/components/ProfessionalProfileAdmin.vue';
import HomeFixPackage from '@/components/HomeFixPackage.vue';
import ClosedAdminServicePackage from '@/components/ClosedAdminServicePackage.vue';
import AdminHomeFixPackage from '@/components/AdminHomeFixPackage.vue';
import UpdateHomeFixPackage from '@/components/UpdateHomeFixPackage.vue';
import CompletedServiceRequest from '@/components/CompletedServiceRequest.vue';
import CompletedServicePackage from '@/components/CompletedServicePackage.vue';
import CompletedHomeFixPackage from '@/components/CompletedHomeFixPackage.vue';
import ActiveServiceRequests from '@/components/ActiveServiceRequests.vue';
import ActiveServicePackages from '@/components/ActiveServicePackages.vue';
import ActiveHomeFixPackage from '@/components/ActiveHomeFixPackage.vue';
import CompletedProfessionalServiceRequest from '@/components/CompletedProfessionalServiceRequest.vue';
import CompletedProfessionalServicePackage from '@/components/CompletedProfessionalServicePackage.vue';
import CompletedProfessionalHomeFixPackage from '@/components/CompletedProfessionalHomeFixPackage.vue';
import ProfessionalPackages from '@/components/ProfessionalPackages.vue';
import UpdateProfessionalPackage from '@/components/UpdateProfessionalPackage.vue';
import UpdateCustomer from '@/components/UpdateCustomer.vue';
import UpdateProfessional from '@/components/UpdateProfessional.vue';
import About from '@/components/About.vue';
import UpdateServiceRequest from '@/components/UpdateServiceRequest.vue';
import ReviewsPage from '@/components/ReviewsPage.vue';
import ReviewCustomer from '@/components/ReviewCustomer.vue';


const routes = [
  {
    path: '/admin_signup',
    name: 'AdminSignup',
    component: AdminSignup,
  },
  {
    path: '/admin_login',
    name: 'AdminLogin',
    component: AdminLogin,
  },
  {
    path:'/customer_login',
    name:'CustomerLogin',
    component:CustomerLogin,
  },
  {
    path:'/customer_signup',
    name:'CustomerSignup',
    component:CustomerSignup,
  },
  {
    path:'/serviceprofessional_login',
    name:'ServiceProfessionalLogin',
    component:ServiceProfessionalLogin,
  },
  {
    path:'/serviceprofessional_signup',
    name:'ServiceProfessionalSignup',
    component:ServiceProfessionalSignup,
  },
  {
    path:'/',
    name:'IndexFirst',
    component:IndexFirst,
  },
  {
    path:'/admin_dashboard',
    name:'AdminDashboard',
    component:AdminDashboard,
    meta:{
      requiresAuth:true,
      role:'Admin',
    }
  },
  {
    path:'/customer_dashboard',
    name:'CustomerDashboard',
    component:CustomerDashboard,
    meta:{
      requiresAuth:true,
      role:'Customer',
    }
  },
  {
    path:'/serviceprofessional_dashboard',
    name:'ServiceProfessionalDashboard',
    component:ServiceProfessionalDashboard,
    meta:{
      requiresAuth:true,
      role:'ServiceProfessional'
    }
  },
  {
    path:'/service-request/:serviceName',
    name:'ServiceRequest',
    component:ServiceRequest,
    props:true,
  },
  {
    path:'/professional/:professionalId',
    name:'ProfessionalProfile',
    component:ProfessionalProfile,
    props:true,
  },
  {
    path:'/service_requests/:requestId/close',
    name:'CloseServiceRequest',
    component:CloseServiceRequest,
    props:true,
  },
  {
    path:'/create_service_package',
    name:'CreateServicePackage',
    component:CreateServicePackage
  },
  {
    path:'/show_customer_package',
    name:'ShowCustomerPackage',
    component:ShowCustomerPackage
  },
  {
    path:'/close-package/:pkgId',
    name:'ClosePackage',
    component:ClosePackage
  },
  {
    path:'/edit-service-request/:requestId',
    name:'EditServiceRequest',
    component:EditServiceRequest
  },
  {
    path:'/requested-services/service-requests',
    name:'ActiveServiceRequests',
    component:ActiveServiceRequests
  },
  {
    path:'/requested-services/service-packages',
    name:'ActiveServicePackages',
    component:ActiveServicePackages
  },
  {
    path:'/requested-services/homefix-packages',
    name:'ActiveHomeFixPackages',
    component:ActiveHomeFixPackage
  },
  {
    path:'/completed-requests/service-requests',
    name:'serviceRequests',
    component:CompletedServiceRequest
  },
  {
    path:'/completed-requests/service-packages',
    name:'servicePackages',
    component:CompletedServicePackage
  },
  {
    path:'/completed-requests/homefix-packages',
    name:'homefixPackages',
    component:CompletedHomeFixPackage
  },
  {
    path:'/admin/blocks',
    name:'BlockManagement',
    component:BlockManagement
  },
  {
    path:'/admin/professional-approvals',
    name:'ProfessionalApprovals',
    component:ProfessionalApprovals
  },
  {
    path:'/documents',
    name:'DocumentsPage',
    component:DocumentRequestForm
  },
  {
    path:'/documentspage',
    name:'DocumentAdminPage',
    component:DocumentPage
  },
  {
    path:'/adminservicepackage',
    name:'AdminServicePackage',
    component:AdminServicePackage
  },
  {
    path:'/admin/professional/:id',
    name:'ProfessionalProfileAdmin',
    component:ProfessionalProfileAdmin
  },
  {
    path:'/homefixpackage',
    name:'HomeFixPackage',
    component:HomeFixPackage
  },
  {
    path:'/close-package-admin/:pkgId',
    name:'CloseAdminPackage',
    component:ClosedAdminServicePackage
  },
  {
    path:'/admin/homefix-packages',
    name:'AdminHomeFixPackage',
    component:AdminHomeFixPackage
  },
  {
    path:'/admin/packages/update/:pkgId',
    name:'HomeFixUpdatePackage',
    component:UpdateHomeFixPackage
  },
  {
    path:'/professional/completed-requested/service-requests',
    name:'professionalserviceRequests',
    component:CompletedProfessionalServiceRequest

  },
  {
    path:'/professional/completed-requested/service-packages',
    name:'professionalservicePackages',
    component:CompletedProfessionalServicePackage

  },
  {
    path:'/professional/completed-requested/homefix-packages',
    name:'professionalhomefixPackages',
    component:CompletedProfessionalHomeFixPackage

  },
  {
    path:'/professional/service-packages',
    name:'ServiceProfessionalPackage',
    component:ProfessionalPackages
  },
  {
    path:'/professional/update-packages/:pkgId',
    name:'ProfessionalUpdatePackage',
    component:UpdateProfessionalPackage
  },
  {
    path:'/update_customer_profile',
    name:'UpdateCustomerProfile',
    component:UpdateCustomer
  },
  {
    path:'/update_profesional_profile',
    name:'UpdateProfessionalProfile',
    component:UpdateProfessional
  },
  {
    path:'/about',
    name:'About',
    component:About
  },
  {
    path:'/update/service_requests',
    name:'UpdateServiceRequest',
    component:UpdateServiceRequest
  },
  {
    path:'/professional/reviews/:id',
    name:'ReviewsPage',
    component:ReviewsPage
  },
  {
    path:'/customer/reviews/:id',
    name:'ReviewsCustomerPage',
    component:ReviewCustomer
  }
  
  // Add more routes as needed
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to,from,next)=>{
  const isAuthenticated=localStorage.getItem('isAuthenticated')=='true';
  const userRole=localStorage.getItem('role')

  if(to.meta.requiresAuth && !isAuthenticated){
    
    if(to.path.startsWith('/admin')){
      next('/admin_login');
    }
    else if(to.path.startsWith('/customer')){
      next('/customer_login');
    }
    else{
      next('/serviceprofessional_login');
    }
  }
  else if(to.meta.role && to.meta.role!=userRole){
    next('/');
  }
  else{
    next();
  }

})

export default router;