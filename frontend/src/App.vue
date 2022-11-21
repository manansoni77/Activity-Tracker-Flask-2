<template>
  <div id="app">
    <TopNavbarVue/>
    <router-view />
  </div>
</template>

<script>
import TopNavbarVue from './TopNavbar.vue';

export default {
  components: {
    TopNavbarVue,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #05386b !important;
  background-color: #5cdb95;
  font-weight: 400;
  font-size: large;
  min-height: 100vh;
}

.form-container {
  max-width: 400px;
  padding: 20px;
  margin: 0 auto;
}

.form-group {
  padding: 10px;
}

.btn {
  min-width: 75px;
}

#addButton {
  color: #05386b;
  border-color: #05386b;
  background-color: transparent;
  padding: 10px;
}

#addButton:hover {
  background-color: #05386b;
  color: #edf5e1;
}

#chart {
  background-color: white;
}

h3 {
  padding: 10px;
}

p {
  color: #edf5e1;
  padding: 5px;
}

</style>
