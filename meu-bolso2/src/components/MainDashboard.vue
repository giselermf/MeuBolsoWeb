<template>
  <div>
    <date-range ref="date_range" :dateFromDelta="-6" :dateToDelta="0" @date_range_updated="getData"></date-range>

    <v-layout row wrap>
      <v-flex xs12 sm6 md6>
        <meu-bolso-bar :height="300" :chartData="barChartData" :title="title"></meu-bolso-bar>
      </v-flex>
      <v-flex xs12 sm6 md6>
        <drill-down-with-table :allData="allData"></drill-down-with-table>
      </v-flex>
    </v-layout>

    <v-layout row wrap>
      <v-flex xs12 sm6 md6>
        <RunningBalanceChart ref="runningBalanceChart" :allData="allData"></RunningBalanceChart>
      </v-flex>
      <v-flex xs12 sm6 md6>
        <v-data-table :headers="estateHeaders" :items="estateData" class="elevation-1">
          <template v-slot:items="props">
            <td class="text-xs-right">{{ props.item.BankName }}</td>
            <td class="text-xs-right">{{ props.item.Date }}</td>
            <td class="text-xs-right">{{ props.item.RunningBalance }}</td>
          </template>
        </v-data-table>
      </v-flex>
    </v-layout>
  </div>
</template>

<script>
import meuBolsoBar from "../charts/MeuBolsoBar.js";
import DrillDownWithTable from "../charts/DrillDownPieWithTable.vue";
import DateRange from "../util/DateRange.vue";
import { HTTP } from "../util/http-common";
import RunningBalanceChart from "../charts/RunningBalanceChart.vue";

import {
  getGroupByMonthAnd,
  getLabelAndDatabaseBar,
  colors
} from "../util/Utils.js";

export default {
  components: {
    meuBolsoBar,
    DrillDownWithTable,
    DateRange,
    RunningBalanceChart
  },
  data() {
    return {
      allData: [],
      barChartData: {},
      title: "Net Over Monhts",
      estateData: [],
      estateHeaders: [
        { value: "BankName", text: "Bank" },
        { value: "Date", text: "Date" },
        { value: "RunningBalance", text: "Current Balance" }
      ]
    };
  },
  mounted() {
    this.getData();
    this.getStateData();
  },
  methods: {
    getParams() {
      return "?filter=" + this.$refs.cashFlow_range.getDateParams();
    },
    getFilterParams() {
      let params = {};
      params["bankName"] = this.selectedAccount;
      params["fromDate"] = this.$refs.date_range.getFromDate();
      params["toDate"] = this.$refs.date_range.getToDate();
      return params;
    },
    getData() {
      HTTP({
        method: "get",
        url:
          "transactionsFiltered/?sort=BankName|asc&filter=" +
          JSON.stringify(this.getFilterParams())
      })
        .then(response => {
          this.allData = response["data"]["data"];
          this.setBarChartData();
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    getStateData() {
      HTTP({
        method: "get",
        url: "estate/"
      })
        .then(response => {
          this.estateData = response["data"]["data"];
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
    },
    search(filterParams) {
      this.getData();
    }
  }
};
</script>

<style>
table.v-table tbody td, table.v-table tbody th {
    height: 31px;
}
</style>
