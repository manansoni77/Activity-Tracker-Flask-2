<template>
  <div>
    <b-navbar variant="light">
      <b-navbar-nav>
        <b-nav-item to="/">HOME</b-nav-item>
        <b-nav-item v-if="LoginStatus" to="/dashboard">DASHBOARD</b-nav-item>
      </b-navbar-nav>
      <b-navbar-nav class="ms-auto">
        <b-nav-item v-if="!LoginStatus" to="/login">LOGIN</b-nav-item>
        <b-nav-item v-if="!LoginStatus" to="/signup">SIGNUP</b-nav-item>
        <b-nav-item v-if="LoginStatus" to="/login">LOGOUT</b-nav-item>
      </b-navbar-nav>
    </b-navbar>
  </div>
</template>

<script>

export default {
  name: 'TopNavBar',
  computed: {
    LoginStatus() {
      return this.$store.state.login_status;
    },
  },
};

</script>

<style scoped>

.navbar {
  padding: 10px 10px;
  background-color: #8ee4af !important;
}
.navbar-nav {
  padding: 0 15px;
}

.nav-link {
  font-weight: bolder;
  color: #ff0000;
}

</style>
