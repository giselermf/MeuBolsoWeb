<template>
  <div>
    <date-range ref="date_range" :dateFromDelta="-6" :dateToDelta="0" @date_range_updated="getData"></date-range>

    <v-layout row wrap>
      <v-flex xs12 sm6 md6>
        <meu-bolso-bar :height="300" :chartData="barChartData" :title="'Net Over Monhts'"></meu-bolso-bar>
      </v-flex>
      <v-flex xs12 sm6 md6>
        <drill-down-with-table :allData="allData"></drill-down-with-table>
      </v-flex>
    </v-layout>
  </div>
</template>

<script>
import meuBolsoBar from "../charts/MeuBolsoBar.js";
import DrillDownWithTable from "../charts/DrillDownPieWithTable.vue";
import DateRange from "../util/DateRange.vue";
import { HTTP } from "../util/http-common";

import {
  getGroupByMonthAnd,
  getLabelAndDatabaseBar,
  colors
} from "../util/Utils.js";

export default {
  components: {
    meuBolsoBar,
    DrillDownWithTable,
    DateRange
  },
  data() {
    return {
      allData: [],
      barChartData: {}
    };
  },
  methods: {
    getParams() {
      let params = {};
      params["fromDate"] = this.$refs.date_range.getFromDate();
      params["toDate"] = this.$refs.date_range.getToDate();
      return "?filter=" + JSON.stringify(params);
    },
    getData() {
      HTTP.get("transactionsFiltered/" + this.getParams())
        .then(response => {
          this.allData = response["data"]["data"];
          this.setBarChartData();
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    setBarChartData() {
      let groupedData = getGroupByMonthAnd(this.allData, "Type");

      for (let e in groupedData) {
        let result = { Net: 0, Income: 0, Expense: 0 };
        for (let x in groupedData[e]) {
          if (groupedData[e][x] > 0) result["Income"] += groupedData[e][x];
          else result["Expense"] += groupedData[e][x];
          result["Net"] += groupedData[e][x];
        }
        groupedData[e] = result;
      }
      this.barChartData = getLabelAndDatabaseBar(groupedData, ["Red", "Green"]);

      // net dataset is line
      for (let x in this.barChartData.datasets) {
        if (this.barChartData.datasets[x].label == "Net") {
          let netDataset = this.barChartData.datasets[x];
          netDataset.borderColor = "black";
          netDataset.pointBorderWidth = 10;
          netDataset.type = "line";
          netDataset.backgroundColor = "black";
        }
      }
    }
  }
};
</script>

<style>
table.v-table tbody td,
table.v-table tbody th {
  height: 31px;
}
</style>
