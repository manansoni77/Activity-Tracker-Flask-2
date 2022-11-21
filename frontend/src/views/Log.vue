<template>
  <div>
    <LogForm :request="request" :log_id="log_id" :track_id="track_id" />
  </div>
</template>

<script>
// @ is an alias to /src
import LogForm from '@/components/LogForm.vue';

export default {
  name: 'Log',
  data() {
    return {
      log_id: null,
      track_id: null,
      track_type: null,
      request: 'add',
    };
  },
  created() {
    this.log_id = this.$route.params.log_id;
    this.track_id = this.$route.params.track_id;
    if (this.log_id) {
      this.request = 'edit';
    }
  },
  components: {
    LogForm,
  },
};
</script>
