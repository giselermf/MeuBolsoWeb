<template>
<div id="app" class="ui vertical segments" >
      <div class="ui  segment">
        <div>
            <label class="form-label">Date:</label>
            <input placeholder="from" v-model="fromDate" class="form-field-small"/> 
            <input placeholder="to" v-model="toDate" class="form-field-small"/> 
            <button type="button" @click="search()" >Search</button>
        </div>
        <div>
          <h2>Net Income</h2>
          <meu-bolso-bar :width="500" :height="300" :chartData="barChartData"></meu-bolso-bar>
          <category-drill-down :width="200" :height="200" :allData="allData" :title="incomeTitle" :positives="true" ></category-drill-down>
          <category-drill-down  :width="200" :height="200" :allData="allData" :title="expenseTitle" :positives="false" ></category-drill-down>
        </div>
      </div>
</div>
</template>

<script>
import meuBolsoBar from "../charts/meuBolsoBar.js";
import CategoryDrillDown from "../charts/CategoryDrillDown.js";
import moment from "moment";
import {
  getGroupByMonthAnd,
  getLabelAndDatabaseBar, colors
} from "../charts/ChartUtils.js";



export default {
  components: {
    meuBolsoBar,
    CategoryDrillDown
  },
  data() {
    return {
      allData: [],
      toDate: null,
      fromDate: null,
      barChartData: {},
      incomeTitle : "Incomes", 
      expenseTitle : "Expenses"
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

