import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

export const DASHBOARD_SCREEN = "DASHBOARD_SCREEN";
export const ACCOUNT_SETTING_SCREEN = "ACCOUNT_SETTING_SCREEN";

export const SHOP_SCREEN = "SHOP_SCREEN";
export const PRODUCT_SCREEN = "PRODUCT_SCREEN";
export const EMPTY_CART_SCREEN = "EMPTY_CART_SCREEN";
export const CART_SCREEN = "CART_SCREEN";
export const CHECKOUT_SCREEN = "CHECKOUT_SCREEN";
export const PLACE_ORDER_SCREEN = "PLACE_ORDER_SCREEN";


const routes = [
  {
    path: "/about",
    name: "About",
    component: () => import("../views/About.vue"),
    meta: {
      isAuthenticated: false,
      guard: "Guest",
    },
  },
  {
    path: "/dashboard/page=:page",
    name: "Dashboard",
    props: true,
    meta: {
      isAuthenticated: true,
      guard: "User",
    },
    component: () => import("../views/Dashboard.vue"),
  },
  // {
  //   path: "/",
  //   name: "Home",
  //   redirect: (to) => {
  //     return { path: "/dashboard/page=1" };
  //   },
  //   component: () => import("../views/Dashboard.vue"),
  //   meta: {
  //     isAuthenticated: true,
  //     guard: "User",
  //   },
  // },
  {
    path: "/shop/page=:page",
    name: "Shop",
    props: true,
    meta: {
      isAuthenticated: true,
      guard: "User",
    },
    component: () => import("../views/Shop.vue"),
  },
  {
    path: "/shopping-cart",
    name: "shopping-cart",
    meta: {
      isAuthenticated: true,
      guard: "User",
    },
    component: () => import("../views/ShoppingCart.vue"),
  },
  {
    path: "/empty-shopping-cart",
    name: "empty-shopping-cart",
    component: () => import("../views/EmptyShoppingCart.vue"),
    meta: {
      isAuthenticated: true,
      guard: "User",
    },
  },
  {
    path: "/checkout",
    name: "CheckOut",
    meta: {
      isAuthenticated: true,
      guard: "User",
    },
    component: () => import("../views/CheckOut.vue"),
  },
  {
    path: "/place-order",
    name: "PlaceOrder",
    meta: {
      isAuthenticated: true,
      guard: "User",
    },
    component: () => import("../views/PlaceOrder.vue"),
  },
  {
    path: "/checkout-payment-complete",
    name: "Checkout Payment",
    meta: {
      isAuthenticated: true,
      guard: "User",
    },
    component: () => import("../views/CheckoutPaymentComplete.vue"),
  },
  {
    path: "/product-details/:productId",
    name: "product-details",
    props: true,
    meta: {
      isAuthenticated: true,
      guard: "User",
    },
    component: () => import("../views/ProductDetails.vue"),
  },
  {
    path: "/my-order/page=:page",
    name: "My Order",
    props: true,
    meta: {
      isAuthenticated: true,
      guard: "User",
    },
    component: () => import("../views/MyOrders.vue"),
  },
  {
    path: "/my-patients/page=:page",
    name: "My Patient",
    props: true,
    meta: {
      isAuthenticated: true,
      guard: "User",
    },
    component: () => import("../views/MyPatient"),
  },
  {
    path: "/help-center",
    name: "Help Center",
    component: () => import("../views/HelpCenter.vue"),
    meta: {
      isAuthenticated: true,
      guard: "User",
    },
  },
  {
    path: "/deals-and-offers",
    name: "Deals and Offers",
    component: () => import("../views/DealsAndOffers.vue"),
    meta: {
      isAuthenticated: true,
      guard: "User",
    },
  },
  {
    path: "/account-settings",
    name: "Account Settings",
    meta: {
      isAuthenticated: true,
      guard: "User",
    },
    component: () => import("../views/AccountSettings.vue"),
  },
  {
    path: "/start-service-existing/page=:page",
    name: "Start Existing Services",
    props: true,
    meta: {
      isAuthenticated: true,
      guard: "User",
    },
    component: () => import("../views/StartServiceExisting.vue"),
  },
  {
    path: "/start-new-ai-service/:productId",
    name: "Start New AI Service",
    props: true,
    meta: {
      isAuthenticated: true,
      guard: "User",
    },
    component: () => import("../views/StartNewAIService.vue"),
  },
  {
    path: "/start-ceph-service-analysis/:type/id=:id",
    name: "Start New Ceph Service analysis",
    props: true,
    meta: {
      isAuthenticated: true,
      guard: "User",
    },
    component: () => import("../views/StartCephServiceAnalysis.vue"),
  },
  {
    path: "/start-Panoramic-analysis/:type/id=:id/patient=:patient",
    name: "Start New Panoramic Service analysis",
    props: true,
    meta: {
      isAuthenticated: true,
      guard: "User",
    },
    component: () => import("../views/StartPanoramaServiceAnalysis.vue"),
  },
  {
    path: "/start-digital-service/:productId",
    name: "start_digital_service",
    props: true,
    meta: {
      isAuthenticated: true,
      guard: "User",
    },
    component: () => import("../views/StartDigitalService.vue"),
  },
  {
    path: "/continue-service-flow/:type/:index",
    name: "continue-service-flow",
    props: true,
    meta: {
      isAuthenticated: true,
      guard: "User",
    },
    component: () => import("../views/NewServiceFlow.vue"),
  },

  {
    path: "/orthodontic-records/:productId",
    name: "Orthodontic Records",
    props: true,
    meta: {
      isAuthenticated: true,
      guard: "User",
    },
    component: () => import("../views/StartOrthodonticRecords.vue"),
  },
  // Medical Imaging Routes
  {
    path: "/medical-imaging",
    name: "MedicalImagingDashboard",
    meta: {
      isAuthenticated: true,
      guard: "User",
    },
    component: () => import("../views/medical-imaging/MedicalImagingDashboard.vue"),
  },
  {
    path: "/medical-imaging/viewer/:studyUID",
    name: "MedicalImagingViewer",
    props: true,
    meta: {
      isAuthenticated: true,
      guard: "User",
    },
    component: () => import("../views/medical-imaging/MedicalImagingViewer.vue"),
  },
  {
    path: "/patient-service",
    name: "Patient Service",
    component: () => import("../views/PatientServices.vue"),
    meta: {
      isAuthenticated: true,
      guard: "User",
    },
  },
  {
    path: "/server-down",
    name: "Server Down",
    component: () => import("../views/ServerDown.vue"),
    meta: {
      isAuthenticated: false,
      guard: "Guest",
    },
  },
  {
    path: "/internal-doctor/dashboard/page=:page",
    name: "Internal Doctor Dashboard",
    props: true,
    meta: {
      isAuthenticated: true,
      guard: "Internal Doctor",
    },
    component: () => import("../views/internalDoctor/dashboard.vue"),
  },
  {
    path: "/internal-doctor/chats/",
    name: "Internal Doctor Chats",
    props: true,
    meta: {
      isAuthenticated: true,
      guard: "Internal Doctor",
    },
    component: () => import("../views/internalDoctor/Chats.vue"),
  },
  {
    path: "/internal-doctor/service-summery/:serviceId",
    name: "Internal Doctor Service Summery",
    props: true,
    meta: {
      isAuthenticated: true,
      guard: "Internal Doctor",
    },
    component: () => import("../views/internalDoctor/ServiceSummery.vue"),
  },
  // {
  //   path: "*",
  //   name: "Home",
  //   component: () => import("../views/Dashboard.vue"),
  //   meta: {
  //     isAuthenticated: true,
  //     guard: "User",
  //   },
  // },

];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, _, next) => {
  // Voxel3DI Authenticiction
  if (to.meta.isAuthenticated) {
    Vue.auth.isUserAuth((auth) => {
      if (!auth) {
        Vue.auth.tryToLogin();
      }
    })
  }

  // if (to.meta.isAuthenticated) {
  //   if (process.env.VUE_APP_ENABLE_KEYCLOAK == "true" && !Vue.keycloak.authenticated) {
  //     Vue.keycloak.login({
  //       redirectUri: window.location.origin + to.path,
  //     });
  //   }
  // }
  next();
});

export default router;
