<template>
  <div>
    <TrackForm :request="request" :track_id="track_id" />
  </div>
</template>

<script>

import TrackForm from '@/components/TrackForm.vue';

export default {
  name: 'Track',
  data() {
    return {
      track_id: null,
      request: 'add',
    };
  },
  created() {
    this.track_id = this.$route.params.track_id;
    if (this.track_id) {
      this.request = 'edit';
    }
  },
  components: {
    TrackForm,
  },
};
</script>
