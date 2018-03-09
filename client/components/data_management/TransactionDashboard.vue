<template>
<div id="app" class="ui vertical segments" >
    <div id="app" class="ui horizontal segments" >
      <div class="ui  segment">
          <div class="content">
              <h2>Expenses by Category</h2>
              <meu-bolso-pie :width="200" :height="200" :chartData="amountByCategoryChartDataNegative" ></meu-bolso-pie>
              <br>
              <vuetable
                    :data="amountByCategoryTableDataNegative"
                    :api-mode=false
                    table-wrapper="#content"
                    :fields="['Category', 'Value']"
              ></vuetable>
              
          </div>
      </div>
      <div class="ui  segment">
        <div class="content">
              <h2>Income by Category</h2>
              <meu-bolso-pie :width="200" :height="200" :chartData="amountByCategoryChartDataPositive" ></meu-bolso-pie>
              <br>
              <vuetable
                    :data="amountByCategoryTableDataPositive"
                    :api-mode=false
                    table-wrapper="#content"
                    :fields="['Category', 'Value']"
              ></vuetable>
        </div>
      </div>
    </div>
    <div class="ui  segment">
        <div class="content">
          <h2>Type over Months</h2>
          <meu-bolso-bar :width="600" :height="300" :chartData="amountByMonthAndCategoryData" xLabel="yearmonth" datasetLabel="Category"></meu-bolso-bar>
        </div>
        <br>
        <vuetable
                    :data="amountByMonthAndCategoryDataTable"
                    :api-mode=false
                    table-wrapper="#content"
                    :fields="['Year', 'Month', 'Type', 'Value']"
              ></vuetable>

      </div>
</div>
</template>

<script>
import meuBolsoPie from "../charts/MeuBolsoPie.js";
import meuBolsoBar from "../charts/meuBolsoBar.js";
import Vuetable from "vuetable-2/src/components/Vuetable.vue";

import {
  getGroupByMonthAnd,
  getDatasetColors,
  groupDataBy,
  getDataSetPie,
  getLabelAndDatabaseBar,
  colors
} from "../charts/ChartUtils.js";

export default {
  components: {
    meuBolsoPie,
    meuBolsoBar,
    Vuetable
  },
  data() {
    const width = 500;
    const height = width * 0.75;
    return {
      all_data: [],
      appendParams: {},
      amountByCategoryChartDataNegative: {},
      amountByCategoryChartDataPositive: {},
      amountByCategoryTableDataNegative: [],
      amountByCategoryTableDataPositive: [],
      amountByMonthAndCategoryData: {},
      amountByMonthAndCategoryDataTable: [],
    };
  },
  mounted() {
    this.$events.$on("filter-set", eventData => this.onFilterSet(eventData));
    this.$events.$on("filter-reset", e => this.onFilterReset());
    this.getData();
  },
  methods: {
    getParams() {
      let params = {};
      for (let x in this.appendParams.filter) {
        params[x] = this.appendParams.filter[x];
      }
      return "?filter=" + JSON.stringify(params);
    },
    getData() {
      let axios = require("axios");
      let querystring = require("querystring");
      axios
        .get("http://127.0.0.1:5000/transactionsFiltered/" + this.getParams())
        .then(response => {
          this.all_data = response["data"]["data"];
          this.getAmountByCategory();
          this.getOverMonth();
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    getOverMonth() {
      let groupedData = getGroupByMonthAnd(this.all_data, "Type");
      //chart data
      this.amountByMonthAndCategoryData = getLabelAndDatabaseBar(groupedData,colors);
      //table data
      this.amountByMonthAndCategoryDataTable.splice(0,this.amountByMonthAndCategoryDataTable.length);
      for (let x in groupedData) {
          let year_month = x.split("/");
            for (let y in groupedData[x]) {
              let oneEntry = {Year: year_month[0], Month: year_month[1], Type: y, Value: groupedData[x][y]};
              this.amountByMonthAndCategoryDataTable.push(oneEntry);
            }
          };
    },
    getAmountByCategory() {
      let groupedData = groupDataBy(this.all_data, "Category");
      this.amountByCategoryChartDataNegative = getDataSetPie(
        groupedData.labels,
        groupedData.values_negatives
      );
      this.amountByCategoryChartDataPositive = getDataSetPie(
        groupedData.labels,
        groupedData.values_positives
      );
      //clean arrays
      this.amountByCategoryTableDataNegative.splice(0,this.amountByCategoryTableDataNegative.length);
      this.amountByCategoryTableDataPositive.splice(0,this.amountByCategoryTableDataPositive.length);
      for (let x in groupedData.labels) {
        if (groupedData.values_negatives[x] != null)
          this.amountByCategoryTableDataNegative.push({
            Category: groupedData.labels[x],
            Value: groupedData.values_negatives[x]
          });
        if (groupedData.values_positives[x] != null)
          this.amountByCategoryTableDataPositive.push({
            Category: groupedData.labels[x],
            Value: groupedData.values_positives[x]
          });
      }
    },
    onFilterSet(filterParams) {
      this.appendParams.filter = filterParams;
      this.getData();
    },
    onFilterReset() {
      delete this.appendParams.filter;
      this.getData();
    }
  }
};
</script>

