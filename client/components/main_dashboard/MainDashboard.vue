<template>
<div id="app" class="ui vertical segments" >
      <div class="ui  segment">
        <div>
            <label class="inline-block">Date:</label>
              <datepicker class="date-picker inline-block" v-model="fromDate" placeholder="from" :minimumView="'month'" :maximumView="'month'"></datepicker>
              <datepicker class="date-picker inline-block" v-model="toDate" placeholder="to" :minimumView="'month'" :maximumView="'month'"></datepicker>
            <a class="button is-primary" @click="search()" >Search</a>
        </div>
      </div>
      <div id="app" class="ui horizontal segments" >
            <div class="ui  segment">
              <meu-bolso-bar :height="300" :chartData="barChartData" :title="title" ></meu-bolso-bar>
              <br>
            </div>
            <div class="ui  segment">
               <drill-down-with-table :allData="allData"></drill-down-with-table>
            </div>
      </div>
      <div id="app" class="ui horizontal segments twelve wide column ">
      <running-balance  :height="500" :allData="allData"></running-balance>>
      </div>
</div>
</template>

<script>
import meuBolsoBar from "../charts/meuBolsoBar.js";
import DrillDownWithTable from "../data_management/DrillDownPieWithTable";
import RunningBalance from "../data_management/RunningBalance";
import Datepicker from "vuejs-datepicker";

import moment from "moment";
import {
  getGroupByMonthAnd,
  getLabelAndDatabaseBar, colors
} from "../util/Utils.js";

export default {
  components: {
    meuBolsoBar,
    DrillDownWithTable,
    RunningBalance,Datepicker
  },
  data() {
    return {
      allData: [],
      toDate: null,
      fromDate: null,
      barChartData: {},
      incomeTitle : "Incomes", 
      expenseTitle : "Expenses",
      grouper: "Type",
      title: "Net Over Monhts"
    };
  },
  mounted() {
    this.fromDate = moment(new Date())
      .subtract(6, "month")
      .startOf("month")
      .format("YYYY-MM-DD");
    this.toDate = moment(new Date()).format("YYYY-MM-DD");
    this.getData();
  },
  methods: {
    getParams() {
      let params = {};
      if (this.fromDate) params["fromDate"] = this.fromDate;
      if (this.toDate) params["toDate"] = this.toDate;
      return "?filter=" + JSON.stringify(params);
    },
    getData() {
      let axios = require("axios");
      let querystring = require("querystring");
      axios
        .get("http://127.0.0.1:5000/transactionsFiltered/" + this.getParams())
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
      this.barChartData = getLabelAndDatabaseBar(groupedData, ["Red","Green"]);

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

