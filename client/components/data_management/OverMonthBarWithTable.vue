<template>
<div >
    <meu-bolso-bar :width="width" :height="height" :chartData="chartData" xLabel="yearmonth" datasetLabel="grouper" :title="title" ></meu-bolso-bar>  
    <div v-if="showTable" class="ui  segment">
      <vuetable
            :data="tableData"
            :api-mode=false
            table-wrapper="#content"
            :fields="['YearMonth', 'Desc', 'Value']"
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
  props: ["allData", "width", "height", "showTable", "grouper"],
  data() {
    const width = 500;
    const height = width * 0.75;
    return {
      all_data: [],
      appendParams: {},
      chartData: {},
      tableData: [],
      title: this.grouper + " Over Months"
    };
  },
  watch: {
    allData: {
      handler(newData, oldData) {
        this.getOverMonth();
      }
    },
    grouper: {
      handler(newData, oldData) {
        this.getOverMonth();
      }
    }
  },
  methods: {
    getOverMonth() {
      console.log(this.grouper)
      let groupedData = getGroupByMonthAnd(this.allData, this.grouper);
      //chart data
      this.chartData = getLabelAndDatabaseBar(groupedData, colors);
      //table data
      this.tableData.splice(0, this.tableData.length);
      for (let x in groupedData) {
        let year_month = x.split("/");
        for (let y in groupedData[x]) {
          let oneEntry = {
            YearMonth: year_month[0] + "/" + year_month[1], 
            Desc: y,
            Value: groupedData[x][y]
          };
          this.tableData.push(oneEntry);
        }
      }
    }
  }
};
</script>

