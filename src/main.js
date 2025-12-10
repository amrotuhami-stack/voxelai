import 'bootstrap/scss/bootstrap.scss'
import 'bootstrap-vue/dist/bootstrap-vue.css'

//import '/src/assets/sccs/utility/_variables.scss'

import authentication from '@/plugins/keycloak.js'
import AuthenticationPlugin from '@/plugins/authentication.js'
import i18n from '@/common/i18n'

import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import vSelect from 'vue-select'
import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { fab } from '@fortawesome/free-brands-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import VueScrollbar from 'vue-scrollbar-live';
import store from '@/store';
import VueIframe from 'vue-iframes';
import moment from 'moment';
import VueSkeletonLoader from 'skeleton-loader-vue';

import VueCountryCode from "vue-country-code";
import VueTelInput from 'vue-tel-input';
import 'vue-tel-input/dist/vue-tel-input.css';

import BaseCarousel from '@/common/components/base/BaseCarousel.vue'
import BaseInnerScrollbar from '@/common/components/base/BaseSmoothScrollbar.vue';

import GTMVue from 'gtm-vue';
Vue.use(GTMVue, {
    // id: process.env.VUE_APP_GTM_ID,
    id: "GTM-K3M76B3",
    defer: false,
    enabled: true,
    debug: false,
    loadScript: true,
    vueRouter: router,
    trackOnNextTick: false,
});


Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
library.add(fas)
library.add(fab)
Vue.use(VueIframe)
Vue.config.productionTip = false;

Vue.filter('formatDate', function(value) {
    if (value) {
        let dateAndTime = value.split('T');
        return `${dateAndTime[0]}  ${dateAndTime[1].split('.')[0].slice(0,5)}`
    }
});

Vue.component('carousel', BaseCarousel)
Vue.component('base-inner-scrollbar', BaseInnerScrollbar)
Vue.component('svg-icon', SvgIcon)
Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.component('VSelect', VSelect)
Vue.component('vue-select', vSelect)
Vue.component('scrollbar', VueScrollbar);
Vue.component('vue-skeleton-loader', VueSkeletonLoader);



import 'bootstrap/scss/bootstrap.scss'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import SvgIcon from '@/common/components/base/BaseSvgIcon.vue'
import VSelect from '@alfsnd/vue-bootstrap-select'


Vue.use(VueCountryCode);
//Vue.use(VueTelInput);

// Vue.use(authentication)
// Vue.keycloak.init({ checkLoginIframe: false }).then((auth) => {
//     // [1] Initialize App
//     new Vue({
//         router,
//         store,
//         i18n,
//         render: (h) => h(App),
//     }).$mount("#app");

//     // [2] Token Refresh
//     Vue.listenToTokenRefresh(6000)

// }).catch(() => {
//     console.log('Failed to obtain token');
// })

Vue.use(AuthenticationPlugin);
new Vue({
  router,
  store,
  i18n,
  render: (h) => h(App),
}).$mount("#app");