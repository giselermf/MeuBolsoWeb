<template>
<div >
    <h2>Type over Months</h2>
    <meu-bolso-bar :width="width" :height="height" :chartData="chartData" xLabel="yearmonth" datasetLabel="Category"></meu-bolso-bar>  
    <div v-if="showTable" class="ui  segment">
      <vuetable
            :data="tableData"
            :api-mode=false
            table-wrapper="#content"
            :fields="['Year', 'Month', 'Type', 'Value']"
      ></vuetable> 
    </div>
</div>
</template>

<script>
import meuBolsoBar from "../charts/meuBolsoBar.js";
import Vuetable from "vuetable-2/src/components/Vuetable.vue";

import {
  getGroupByMonthAnd,
  getLabelAndDatabaseBar,
  colors
} from "../charts/ChartUtils.js";

export default {
  components: {
    meuBolsoBar,
    Vuetable
  },
  props: ["allData", "width", "height", "showTable"],
  data() {
    const width = 500;
    const height = width * 0.75;
    return {
      all_data: [],
      appendParams: {},
      chartData: {},
      tableData: []
    };
  },
  watch: {
    allData: {
      handler(newData, oldData) {
        this.getOverMonth();
      }
    }
  },
  methods: {
    getOverMonth() {
      let groupedData = getGroupByMonthAnd(this.allData, "Type");
      //chart data
      this.chartData = getLabelAndDatabaseBar(groupedData, colors);
      //table data
      this.tableData.splice(0, this.tableData.length);
      for (let x in groupedData) {
        let year_month = x.split("/");
        for (let y in groupedData[x]) {
          let oneEntry = {
            Year: year_month[0],
            Month: year_month[1],
            Type: y,
            Value: groupedData[x][y]
          };
          this.tableData.push(oneEntry);
        }
      }
    }
  }
};
</script>

