import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
import Signup from '../views/Signup.vue';
import Login from '../views/Login.vue';
import Ping from '../components/Ping.vue';
import Dashboard from '../views/Dashboard.vue';
import Track from '../views/Track.vue';
import Log from '../views/Log.vue';
import ViewTrack from '../views/ViewTrack.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/ping',
    name: 'Ping',
    component: Ping,
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Signup,
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
  },
  {
    path: '/track/:track_id',
    name: 'ViewTrack',
    component: ViewTrack,
  },
  {
    path: '/addtrack',
    name: 'AddTrack',
    component: Track,
  },
  {
    path: '/edittrack/:track_id',
    name: 'EditTrack',
    component: Track,
  },
  {
    path: '/logtrack/:track_id',
    name: 'AddLog',
    component: Log,
  },
  {
    path: '/editlog/:log_id',
    name: 'EditLog',
    component: Log,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
