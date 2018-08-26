<template>
<div id="app" class="ui vertical" >
      <div class="field is-grouped">
          <p class="control">
            <date-range ref="cashFlow_range" minimumView="month"></date-range>            
          </p>
          <p class="control">
            <button class="button is-link" @click="search()" >Search</button>
          </p>
      </div>
      <meu-bolso-line :height="300" :chartData="chartData" title="Cash Flow" ></meu-bolso-line>
</div>
</template>

<script>
import DateRange from "../util/DateRange.vue";
import CallServer from "../util/CallServer.js";
import meuBolsoLine from "../charts/meuBolsoLine.js";
import moment from "moment";

export default {
  mixins: [CallServer],
  components: {
    DateRange,
    meuBolsoLine
  },
  data() {
    return {
      chartData: null,
      labels: null,
      values: null
    };
  },

  mounted() {
    this.$refs.cashFlow_range.setRange(0, 6);
    this.$refs.cashFlow_range.fromDate = new Date();
    this.getAllData("cashFlow", this.getParams());
    this.getRunningBalance(this.$refs.cashFlow_range.fromDate);
  },
  watch: {
    allData: {
      handler(newData, oldData) {
        this.getChartData();
      }
    }
  },
  methods: {
    search(filterParams) {
      this.getAllData("cashFlow", this.getParams());
      this.getRunningBalance(this.$refs.cashFlow_range.fromDate);
    },
    getParams() {
      return "?filter=" + this.$refs.cashFlow_range.getDateParams();
    },
    getRunningBalance(fromDate) {
      let params = {};
      if (fromDate) params["byDate"] = fromDate;
      this.axios
        .get(
          this.apiUrl + "RunningBalance/" + "?filter=" + JSON.stringify(params)
        )
        .then(response => {
          this.RunningBalance = response["data"]["data"][0]["balance"];
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    getChartData() {
      let alabels = this.allData.map(x => moment(x.Date));
      let aValues = this.allData.map(x => x.Amount);

      alabels = alabels.map(function(m) {
        return m.format("YYYY-MM-DD");
      });

      for (let index in aValues) {
        if (index > 0) {
          aValues[index] += aValues[index - 1];
        } else {
          aValues[index] += this.RunningBalance;
        }
      }

      this.chartData = {
        labels: alabels,
        datasets: [
          {
            label: "Cash Flow",
            fill: true,
            data: aValues,
            showLine: true
          }
        ]
      };
    }
  }
};
</script>

