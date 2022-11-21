<template>
  <div class="form-container">
    <b-alert v-model="showAlert" variant="danger">
      {{ message }}
    </b-alert>
    <b-form @submit.prevent="signupMethod">
      <b-form-group label="First Name">
        <b-form-input type="text" v-model="first_name" placeholder="Enter your first name" required>
        </b-form-input>
      </b-form-group>
      <b-form-group label="Last Name">
        <b-form-input type="text" v-model="last_name" placeholder="Enter your last name" required>
        </b-form-input>
      </b-form-group>
      <b-form-group label="Email Id">
        <b-form-input type="email" v-model="email_id" placeholder="Enter a unique login id" required>
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
  name: 'SignupForm',
  data() {
    return {
      message: '',
      first_name: '',
      last_name: '',
      email_id: '',
      password: '',
      showAlert: false,
    };
  },
  created() {
    this.$axios.defaults.headers.common['x-access-token'] = this.$store.state.token;
  },
  methods: {
    signupMethod() {
      this.$axios.post('/signup', {
        first_name: this.first_name,
        last_name: this.last_name,
        email_id: this.email_id,
        password: this.password,
      }).then((res) => {
        if (res.status === 201) {
          this.message = res.data.message;
          this.showAlert = true;
          this.$router.push('/login');
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
