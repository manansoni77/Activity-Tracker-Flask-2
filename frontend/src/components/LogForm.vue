<template>
  <div class="form-container">
    <b-alert v-model="showAlert" variant="danger">
      {{ message }}
    </b-alert>
    <b-form @submit.prevent="logMethod">
      <div v-if="track_type === 'num'">
        <b-form-group :label="options">
          <b-form-input type="text" v-model="log_info" placeholder="Enter Action" required>
          </b-form-input>
        </b-form-group>
        <br>
        <b-form-group label="Time of Action">
          <b-form-input type="datetime-local" v-model="log_time" placeholder="Enter Time of Action" required>
          </b-form-input>
        </b-form-group>
      </div>
      <div v-if="track_type === 'mcq'">
        <b-form-group label="Choice">
          <select class="form-control" v-model="log_info">
            <option v-for="option in options" :value="option" :key="option">{{ option }}</option>
          </select>
        </b-form-group>
        <b-form-group label="Time of Action">
          <b-form-input type="datetime-local" v-model="log_time" placeholder="Enter Time of Action" required>
          </b-form-input>
        </b-form-group>
      </div>
      <div v-if="track_type === 'time'">
        <b-form-group label="Start Time">
          <b-form-input type="datetime-local" v-model="log_time" placeholder="Enter Start Time" required>
          </b-form-input>
        </b-form-group>
        <b-form-group label="End Time">
          <b-form-input type="datetime-local" v-model="log_info" placeholder="Enter End Time" required>
          </b-form-input>
        </b-form-group>
      </div>
      <div v-if="track_type === 'bool'">
        <b-form-group label="Choice">
          <select class="form-control" v-model="log_info">
            <option v-for="option in options" :value="option" :key="option">{{ option }}</option>
          </select>
        </b-form-group>
        <b-form-group label="Time of Action">
          <b-form-input type="datetime-local" v-model="log_time" placeholder="Enter Time of Action" required>
          </b-form-input>
        </b-form-group>
      </div>
      <br>
      <b-button id="addButton" pill type="submit">DONE</b-button>
    </b-form>
  </div>
</template>
<script>

export default {
  name: 'LogForm',
  props: ['request', 'log_id', 'track_id'],
  data() {
    return {
      message: '',
      track_type: '',
      options: '',
      log_time: '',
      log_info: '',
      showAlert: false,
    };
  },
  async created() {
    this.$axios.defaults.headers.common['x-access-token'] = this.$store.state.token;
    if (this.request === 'edit') {
      await this.$axios.get(`/get_log/${this.log_id}`).then((res) => {
        this.track_id = res.data.track_id;
        this.log_time = res.data.log_time;
        this.log_info = res.data.log_info;
      });
    }
    this.$axios.get(`/get_track_type/${this.track_id}`).then((res) => {
      this.track_type = res.data.track_type;
      this.options = res.data.options;
      if (this.track_type === 'mcq' || this.track_type === 'bool') {
        this.options = this.options.split(',');
      }
    });
  },
  methods: {
    logMethod() {
      if (this.request === 'add') {
        this.$axios.post('/update_log', {
          track_id: this.track_id,
          track_type: this.track_type,
          log_time: this.log_time,
          log_info: this.log_info,
        }).then((res) => {
          if (res.status === 201) {
            this.$router.push(`/track/${this.track_id}`);
          } else if (res.status === 203) {
            this.message = res.data.message;
            this.showAlert = true;
          }
        }).catch((_err) => {
          this.message = 'Some Error Occured';
          this.showAlert = true;
        });
      } else if (this.request === 'edit') {
        this.$axios.put('/update_log', {
          log_id: this.log_id,
          track_type: this.track_type,
          log_time: this.log_time,
          log_info: this.log_info,
        }).then((res) => {
          if (res.status === 201) {
            this.$router.push(`/track/${this.track_id}`);
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
