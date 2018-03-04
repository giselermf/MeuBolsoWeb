<template>
<div id="app" class="ui vertical segments" >
    <div id="app" class="ui horizontal segments" >
      <div class="ui  segment">
          <div class="content">
              <h2>Amount by Category***</h2>
              <meu-bolso-pie-data :width="200" :height="200" :chartData="amountByCategoryData" ></meu-bolso-pie-data>
          </div>
      </div>
      <div class="ui  segment">
        <div class="content">
          <h2>Amount by Category/Month</h2>
          <meu-bolso-bar :chartData="amountByMonthAndCategoryData" xLabel="yearmonth" datasetLabel="Category"></meu-bolso-bar>
        </div>
      </div>
    </div>
</div>
</template>

<script>
import meuBolsoPieData from "../charts/MeuBolsoPie.js";
import meuBolsoBar from "../charts/meuBolsoBar.js";
import {
  getGroupByMonthAnd,
  getDatasetColors,
  getDataSet,
  groupDataBy
} from "../charts/ChartUtils.js";

export default {
  components: {
    meuBolsoPieData,
    meuBolsoBar
  },
  data() {
    const width = 500;
    const height = width * 0.75;
    return {
      all_data: [],
      appendParams: {},
      chartWidth: width,
      chartHeight: height,
      amountByCategoryData: {},
      amountByMonthAndCategoryData: {}
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
          this.amountByMonthAndCategoryData = getGroupByMonthAnd(
            this.all_data,
            "Type"
          );
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    getAmountByCategory() {
      let result = groupDataBy(this.all_data, "Category");
      this.amountByCategoryData = getDataSet(result.labels, result.values);
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

