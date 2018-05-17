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
      <meu-bolso-bar :height="300" :chartData="chartData" title="Cash Flow" ></meu-bolso-bar>

</div>
</template>

<script>
import DateRange from "../util/DateRange.vue";
import CallServer from "../util/CallServer.js";
import meuBolsoBar from "../charts/meuBolsoBar.js";

export default {
  mixins: [CallServer],
  components: {
    DateRange,
    meuBolsoBar
  },
  data() {
    return {
      chartData: null,
      labels: null,
      values: null,
    };
  },
  mounted() {
    this.$refs.cashFlow_range.setRange(-1,6);
    this.getAllData("cashFlow", this.getParams());
    this.getRunningBalance(this.$refs.cashFlow_range.fromDate);
  },
  watch: {
    allData: function(val) {
      this.setBarChartData();
    },
  },
  methods: {
    getParams() {
      return "?filter=" + this.$refs.cashFlow_range.getDateParams();
    },
    search(filterParams) {
      this.getData(this.allData, "cashFlow", this.getParams());
    },
    getRunningBalanceDataset() {
      let runningValues = [];
      for (let monthIndex in this.labels) {
        this.RunningBalance += this.values[monthIndex]
        runningValues.push(this.RunningBalance )
      }
      let dataset = {}
      dataset["borderColor"] = "black";
      dataset["pointBorderWidth"] = 10;
      dataset["type"] = "line";
      dataset["label"] = "Running Balance";
      dataset['data'] = runningValues
      return dataset;
    },

    setBarChartData() {
      if (this.allData == undefined) return;
      this.labels = this.allData.map(x => x.Month + "/" + x.Year);
      this.values = this.allData.map(x => x.NetInMonth);
      this.chartData = {
        labels: this.labels,
        datasets: [
          {
            label: "Cash Flow",
            borderWidth: 1,
            beginzero: "true",
            fill: false,
            data: this.values
          }, this.getRunningBalanceDataset()
        ]
      };
    }
  }
};
</script>

