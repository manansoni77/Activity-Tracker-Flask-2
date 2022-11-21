import Vue from 'vue';
import moment from 'moment';
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue';
import App from './App.vue';
import router from './router';
import store from './store';
import axiosPlugin from './plugin/axiosPlugin';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

Vue.config.productionTip = false;
Vue.use(axiosPlugin);
Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);

Vue.filter('format_time', (value) => {
  if (value) {
    return moment(String(value)).add(-30, 'm').add(-5, 'h').format('MM/DD/YYYY hh:mm');
  }
  return '';
});

new Vue({
  router,
  store,
  render: (h) => h(App),
  created() {
    this.$setupAxios();
  },
}).$mount('#app');
