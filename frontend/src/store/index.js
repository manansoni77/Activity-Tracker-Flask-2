import Vue from 'vue';
import Vuex from 'vuex';
import VuexPersistence from 'vuex-persist';

const vuexLocal = new VuexPersistence({
  storage: window.localStorage,
});

Vue.use(Vuex);

export default new Vuex.Store({
  plugins: [vuexLocal.plugin],
  state: {
    login_status: false,
    token: '',
  },
  mutations: {
    login(state, token) {
      state.login_status = true;
      state.token = token;
    },
    logout(state) {
      state.login_status = false;
      state.token = '';
    },
  },
});
