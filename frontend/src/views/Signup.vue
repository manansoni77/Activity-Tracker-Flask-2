<template>
    <div>
      <SignupForm />
    </div>
  </template>

<script>
// @ is an alias to /src
import SignupForm from '@/components/SignupForm.vue';

export default {
  name: 'Signup',
  components: {
    SignupForm,
  },
};
</script>
