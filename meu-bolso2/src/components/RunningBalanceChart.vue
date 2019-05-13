<template>
  <v-flex xs12 sm6 md10>
    <meu-bolso-line
      :height=300
      :width=600
      :chartData="chartData"
      :title="title"
      xLabel="Date"
      data-set-label="BankName"
    ></meu-bolso-line>
  </v-flex>
</template>

<script>
import meuBolsoLine from "../charts/MeuBolsoLine.js";
import moment from "moment";
import { colors } from "../util/Utils.js";

export default {
  components: {
    meuBolsoLine
  },
  props: ["allData"],
  data() {
    return {
      title: "Running Balance",
      chartData: {}
    };
  },
  created() {
    this.getChartData();
  },
  watch: {
    allData: {
      handler(newData, oldData) {
        this.getChartData();
      }
    }
  },
  methods: {
    createDataset(alabels, bank, allBankSerie, datasetsLength) {
      let values = [];
      let lastValue = 0;
      for (let x in alabels) {
        let runningDate = alabels[x];
        if (allBankSerie[runningDate] == undefined) {
          values.push(lastValue);
        } else {
          lastValue = allBankSerie[runningDate];
          values.push(allBankSerie[runningDate]);
        }
      }
      return {
        label: bank,
        fill: true,
        //backgroundColor: colors[datasetsLength % colors.length],
        borderColor: colors[datasetsLength % colors.length],
        data: values,
        showLine: true
      };
    },
    getChartData() {
      let datasets = [];

      let alabels = this.allData.map(x => moment(x.Date));

      alabels = alabels.sort(function(a, b) {
        return a - b;
      });

      alabels = alabels.map(function(m) {
        return m.format("YYYY-MM-DD");
      });
      alabels = Array.from(new Set(alabels));

      let groupedData = this.allData.reduce(function(r, a) {
        r[a["BankName"]] = r[a["BankName"]] || {};
        let dateRunning = moment(a.Date).format("YYYY-MM-DD");
        r[a["BankName"]][dateRunning] = Math.round(a.RunningBalance);
        return r;
      }, Object.create(null));

      let runningValues = [];
      for (let bank in groupedData) {
        datasets.push(
          this.createDataset(alabels, bank, groupedData[bank], datasets.length)
        );
      }
      this.chartData = {
        labels: alabels,
        datasets: datasets
      };
    }
  }
};
</script>