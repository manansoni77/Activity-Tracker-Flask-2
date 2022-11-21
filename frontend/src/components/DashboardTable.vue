<template>
  <div>
    <h3>MY TRACKERS</h3>
    <p v-if="tracks.length === 0"> NO TRACKERS YET!</p>
    <b-table-simple v-else>
      <b-thead>
        <b-tr>
          <b-th>Tracker Name</b-th>
          <b-th>Last Log</b-th>
          <b-th>Time</b-th>
          <b-th colspan="3">Actions</b-th>
        </b-tr>
      </b-thead>
      <b-tr v-for="track in tracks" :key="track.track_id">
        <b-td>
          <b-button pill variant="light" @click="goToTrack(track.track_id)">{{ track.track_name }}</b-button>
        </b-td>
        <b-td>
          {{ track.last_log }}
        </b-td>
        <b-td>
          {{ track.time|format_time }}
        </b-td>
        <b-td>
          <b-button pill variant="light" @click="editTrack(track.track_id)">EDIT</b-button>
        </b-td>
        <b-td>
          <b-button pill variant="light" @click="logTrack(track.track_id)">LOG</b-button>
        </b-td>
        <b-td>
          <b-button pill variant="light" @click="deleteTrack(`${track.track_id}`)">DEL</b-button>
        </b-td>
      </b-tr>
    </b-table-simple>
    <p>
      <b-button id="addButton" pill @click="addtrack">ADD TRACK</b-button>
    </p>
  </div>
</template>

<style scoped>

.table {
  color: #edf5e1;
}

table button {
  color: #edf5e1;
  border-color: #edf5e1;
  border-width: 2px !important;
  background-color: transparent;
}

[role=cell] {
  padding: 5px;
}

</style>

<script>

export default {
  name: 'DashboardTable',
  data() {
    return {
      tracks: [],
      message: 'No message',
    };
  },
  created() {
    this.$axios.defaults.headers.common['x-access-token'] = this.$store.state.token;
    this.loadData();
  },
  methods: {
    goToTrack(trackId) {
      this.$router.push(`/track/${trackId}`);
    },
    editTrack(trackId) {
      this.$router.push(`/edittrack/${trackId}`);
    },
    logTrack(trackId) {
      this.$router.push(`/logtrack/${trackId}`);
    },
    deleteTrack(trackId) {
      this.$axios.post(`/delete_tracker/${trackId}`).then((res) => {
        this.loadData();
      });
    },
    addtrack() {
      this.$router.push('/addtrack');
    },
    loadData() {
      this.$axios.get('/dashboard').then((res) => {
        if (res.data) {
          this.tracks = res.data;
        }
      });
    },
  },
};

</script>
