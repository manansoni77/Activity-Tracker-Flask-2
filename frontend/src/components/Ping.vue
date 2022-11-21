<template>
    <div>
        <p>{{ message }}</p>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Ping',
  data() {
    return {
      message: 'Hello! Ping!',
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5000/ping';
      axios.get(path).then((res) => {
        this.message = res.data.msg;
      });
    },
  },
  created() {
    this.getMessage();
  },
};
</script>
