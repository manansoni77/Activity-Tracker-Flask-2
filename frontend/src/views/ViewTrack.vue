<template>
  <div id="container">
    <div id="heading">
      <h1> {{track.track_name}} </h1>
      <h3> {{track.track_desc}} </h3>
      <b-button id="addButton" pill @click="logTrack(track.track_id)">Log Track</b-button>
      <b-button id="addButton" pill @click="getCsv(track.track_id)">Export CSV</b-button>
    </div>
    <div>
      <b-table-simple v-if="logs.length !== 0">
        <b-thead>
          <b-tr>
            <b-th>
              Value
            </b-th>
            <b-th>
              Time
            </b-th>
            <b-th colspan="2">
              Actions
            </b-th>
          </b-tr>
        </b-thead>
        <b-tr v-for="log in logs" :key="log.log_id">
          <b-td>
            {{ log.info }}
          </b-td>
          <b-td>
            {{ log.time|format_time }}
          </b-td>
          <b-td>
            <b-button pill variant="light" @click="editLog(log.log_id)">EDIT</b-button>
          </b-td>
          <b-td>
            <b-button pill variant="light" @click="deleteLog(log.log_id)">DEL</b-button>
          </b-td>
        </b-tr>
      </b-table-simple>
      <p v-else> There are no logs to show </p>
    </div>
    <div id="chartContainer">
      <div v-if="logs.length === 0">
        <p> There is no chart to Show </p>
      </div>
      <div id="chartWrapper" v-else>
        <canvas id="chart"></canvas>
      </div>
    </div>
  </div>
</template>

<style scoped>

#container {
  padding: 10px 20px;
}

#chartContainer {
  padding: 20px 20px;
}

#heading {
  padding: 10px;
}

a {
  padding: 5px 15px;
}

[role=cell] {
  padding: 5px;
}
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

import moment from 'moment';
import Chart from 'chart.js';
import { DataFormat } from '../components/DataFormat';

export default {
  name: 'ViewTrack',
  data() {
    return {
      track: {},
      logs: [],
    };
  },
  created() {
    this.$axios.defaults.headers.common['x-access-token'] = this.$store.state.token;
    this.loadData();
  },
  methods: {
    logTrack(trackId) {
      this.$router.push(`/logtrack/${trackId}`);
    },
    editLog(logId) {
      this.$router.push(`/editlog/${logId}`);
    },
    deleteLog(logId) {
      this.$axios.post(`/delete_log/${logId}`).then((res) => {
        this.loadData();
      });
    },
    getCsv(trackId) {
      this.$axios.get(`/getcsv/${trackId}`);
    },
    async loadData() {
      await this.$axios.get(`/get_trackdata/${this.$route.params.track_id}`).then((res) => {
        this.track = res.data.track;
        this.logs = res.data.logs;
      });
      this.logs.sort((first, second) => (new Date(first.time)).getTime() - (new Date(second.time)).getTime());
      const inpdata = [];
      const inplabel = [];
      let ylabel = 'units';
      let type = 'line';
      if (this.track.track_type === 'num') {
        ylabel = this.track.options;
        this.logs.forEach((element) => {
          inpdata.push(Number(element.info));
          inplabel.push(moment(element.time).format('DD/MM/YYYY'));
        });
      } else if (this.track.track_type === 'time') {
        ylabel = 'Hours';
        this.logs.forEach((element) => {
          const time = moment(element.info, 'hh:mm:ss');
          const hours = time.hour() + time.minute() / 60 + time.second() / 3600;
          inpdata.push(hours);
          inplabel.push(moment(element.time).format('DD/MM/YYYY'));
        });
      } else if (this.track.track_type === 'bool' || this.track.track_type === 'mcq') {
        type = 'pie';
        const freq = {};
        this.logs.forEach((element) => {
          if (freq[element.info]) {
            freq[element.info] += 1;
          } else {
            freq[element.info] = 1;
          }
        });
        for (const k in freq) {
          inplabel.push(k);
          inpdata.push(freq[k]);
        }
      } const ctx = document.getElementById('chart').getContext('2d');
      new Chart(ctx, DataFormat(type, inpdata, inplabel, ylabel));
    },
  },
};
</script>

<style>
#chartWrapper {
  width: 500px !important;
  height: 500px !important;
}
</style>
