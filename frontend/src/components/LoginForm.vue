<template>
  <div class="form-container">
    <b-alert v-model="showAlert" variant="danger">
      {{ message }}
    </b-alert>
    <b-form @submit.prevent="loginMethod">
      <b-form-group label="Email Address">
        <b-form-input type="email" placeholder="Enter your email id" v-model="email_id" required>
        </b-form-input>
      </b-form-group>
      <b-form-group label="Password">
        <b-form-input type="password" placeholder="Enter a STRONG password" v-model="password" required>
        </b-form-input>
      </b-form-group>
      <b-button type="submit" variant="primary">Submit</b-button>
    </b-form>
  </div>
</template>

<script>

export default {
  name: 'LoginForm',
  data() {
    return {
      message: '',
      email_id: '',
      password: '',
      showAlert: false,
      store_test: this.$store.state.test,
    };
  },
  created() {
    this.$store.commit('logout');
  },
  methods: {
    loginMethod() {
      this.$axios.post('/login', {
        email_id: this.email_id,
        password: this.password,
      }).then((res) => {
        if (res.status === 201) {
          this.message = res.data.message;
          this.$store.commit('login', res.data.token);
          this.$router.push('/dashboard');
        } else if (res.status === 203) {
          this.message = res.data.message;
          this.showAlert = true;
        }
      }).catch((_err) => {
        this.message = 'Some Error Occured';
        this.showAlert = true;
      });
    },
  },
};
</script>
