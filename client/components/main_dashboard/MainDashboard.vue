<template>
<div id="app" class="ui vertical" >
      <div class="field is-horizontal-left" >
          <div class="field-body">
              <div class="field is-grouped">
                  <date-range ref="cashFlow_range" minimumView="month"></date-range>
                  <p class="control">
                    <button class="button is-link" @click="search()" >Search</button>
                  </p>
          </div></div>
      </div>

      <div id="app" class="ui horizontal segments" >
        <div class="ui  segment">
          <meu-bolso-bar :height="300" :chartData="barChartData" :title="title" ></meu-bolso-bar>
        </div>
        <div class="ui  segment">
          <drill-down-with-table :allData="allData"></drill-down-with-table>
        </div>
      </div>
      
      <RunningBalanceChart ref="runningBalanceChart" :allData="allData"></RunningBalanceChart>

      <div id="app" class="ui horizontal segments" >
        <div class="ui  segment">
          <my-vuetable ref="vuetableTransaction"
              api-url="http://127.0.0.1:5000/estate/"
              :fields="estate_fields"
          >
          </my-vuetable>

        </div>
      </div>
</div>
</template>

<script>
import meuBolsoBar from "../charts/meuBolsoBar.js";
import DrillDownWithTable from "../transaction/DrillDownPieWithTable.vue";
import DateRange from "../util/DateRange.vue";
import {HTTP} from '../util/http-common';
import RunningBalanceChart from "../transaction/RunningBalanceChart.vue";
import MyVuetable from "../util/MyVuetable.vue";

import {
  getGroupByMonthAnd,
  getLabelAndDatabaseBar, colors
} from "../util/Utils.js";

export default {
  components: {
    meuBolsoBar,MyVuetable,
    DrillDownWithTable,DateRange,RunningBalanceChart
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
      title: "Net Over Monhts",
      httpOptions: {

      },
      estate_fields: [
        {
          name: "BankName",
          title: "Bank",
          titleClass: "center aligned",
          dataClass: "left aligned"
        },
        {
          name: "Date",
          title: "Date",
          titleClass: "center aligned",
          dataClass: "left aligned"
        },
        {
          name: "RunningBalance",
          title: "Current Balance",
          titleClass: "center aligned",
          dataClass: "center aligned",
          callback: "formatFloat"
        }]
    };
  },
  mounted() {
    this.$refs.cashFlow_range.setRange(-6, 0);
    this.getData();
  },
  methods: {
    getParams() {
      return "?filter=" + this.$refs.cashFlow_range.getDateParams();
    },
    getData() {
      HTTP
        .get("transactionsFiltered/" + this.getParams())
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

