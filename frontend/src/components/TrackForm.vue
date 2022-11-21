<template>
  <div class="form-container">
    <b-alert v-model="showAlert" variant="danger">
      {{ message }}
    </b-alert>
    <p>
      When entering options - <br>
      For Multiple Choice enter comma seperated words <br>
      Eg. Happy,Sad,Angry <br>
      For Numerical enter the unit <br>
      Eg. 'Glasses' or 'Celcius' or 'Laps' <br>
      For Bool enter positive and negative <br>
      Eg. Work Done,Procrastinated <br>
      For Time Duration leave the options blank <br>
    </p>
    <b-form @submit.prevent="trackMethod">
      <b-form-group label="Tracker Name">
        <b-form-input type="text" v-model="track_name" placeholder="Enter name of the Tracker" required>
        </b-form-input>
      </b-form-group>
      <b-form-group label="Tracker Description">
        <b-form-input type="text" v-model="track_desc" placeholder="Enter description of the Tracker" required>
        </b-form-input>
        </b-form-group>
      <b-form-group label="Choose Type of Tracker">
        <select class="form-control" v-model="track_type">
          <option value="num">Numerical</option>
          <option value="mcq">Multiple Choice</option>
          <option value="time">Time Duration</option>
          <option value="bool">Boolean</option>
        </select>
      </b-form-group>
      <b-form-group label="Options">
        <b-form-input type="text" v-model="options" placeholder="Enter Your Customisations for the tracker, if any">
        </b-form-input>
        </b-form-group>
      <br>
      <b-button id="addButton" pill type="submit">DONE</b-button>
    </b-form>
  </div>
</template>
<script>

export default {
  name: 'TrackForm',
  props: ['request', 'track_id'],
  data() {
    return {
      message: '',
      track_name: '',
      track_desc: '',
      track_type: '',
      options: '',
      showAlert: false,
    };
  },
  created() {
    this.$axios.defaults.headers.common['x-access-token'] = this.$store.state.token;
    if (this.request === 'edit') {
      this.$axios.get(`/get_track/${this.track_id}`).then((res) => {
        this.track_name = res.data.track_name;
        this.track_desc = res.data.track_desc;
        this.track_type = res.data.track_type;
        this.options = res.data.options;
      });
    }
  },
  methods: {
    trackMethod() {
      if (this.request === 'add') {
        this.$axios.post('/update_tracker', {
          track_name: this.track_name,
          track_desc: this.track_desc,
          track_type: this.track_type,
          options: this.options,
        }).then((res) => {
          if (res.status === 201) {
            this.$router.push('/dashboard');
          } else if (res.status === 203) {
            this.message = res.data.message;
            this.showAlert = true;
          }
        }).catch((_err) => {
          this.message = 'Some Error Occured';
          this.showAlert = true;
        });
      } else if (this.request === 'edit') {
        this.$axios.put('/update_tracker', {
          track_id: this.track_id,
          track_name: this.track_name,
          track_desc: this.track_desc,
          track_type: this.track_type,
          options: this.options,
        }).then((res) => {
          if (res.status === 201) {
            this.$router.push('/dashboard');
          } else if (res.status === 203) {
            this.message = res.data.message;
            this.showAlert = true;
          }
        }).catch((_err) => {
          this.message = 'Some Error Occured';
          this.showAlert = true;
        });
      }
    },
  },
};
</script>
