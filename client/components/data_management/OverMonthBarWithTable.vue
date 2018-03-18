<template>
<div >
    <meu-bolso-bar :width="width" :height="height" :chartData="chartData" xLabel="yearmonth" datasetLabel="grouper" :title="title" ></meu-bolso-bar>  
    <div v-if="showTable && tableFields.length>0" class="ui  segment">
      <vuetable ref="vuetableData"
            :data="tableData"
            :api-mode=false
            table-wrapper="#content"
            :fields="tableFields"
      ></vuetable> 
    </div>
</div>
</template> 

<script>
import meuBolsoBar from "../charts/meuBolsoBar.js";
import Vuetable from "vuetable-2/src/components/Vuetable.vue";
import Vue from "vue";

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
    return {
      title: this.grouper + " Over Months",
      tableFields: [],
      tableData: [],
      chartData: {}
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
    formatValues(value) {
      if (value == 0 || value == null) return "";
      if (value < 0)
        return '<div style="text-align: end;color: red;">' + value + "</span>";
      else
        return (
          '<div style="text-align: end;color: black;">' + value + "</span>"
        );
    },
    getOverMonth() {
      if (this.allData == null) return;
      let rows = {};
      let groupedData = getGroupByMonthAnd(this.allData, this.grouper);
      //chart data
      this.chartData = getLabelAndDatabaseBar(groupedData, colors);

      //clean table data
      this.tableData.splice(0, this.tableData.length);
      //this.tableFields.splice(0, this.tableFields.length);
      this.tableFields = ["Desc"];
      //push data into table data
      for (let col in groupedData) {
        if (this.tableFields.indexOf(col) < 0)
          this.tableFields.push({ name: col, callback: "formatValues" });
        for (let desc in groupedData[col]) {
          if (groupedData[col][desc] != 0) {
            if (desc in rows) {
              rows[desc][col] = groupedData[col][desc];
            } else {
              let newCol = {};
              newCol[col] = groupedData[col][desc];
              rows[desc] = newCol;
            }
          }
        }
      }
      for (let e in rows) {
        rows[e]["Desc"] = e;
        this.tableData.push(rows[e]);
      }
      if (this.$refs.vuetableData) {
        Vue.nextTick(() => this.$refs.vuetableData.normalizeFields());
      }
    }
  }
};
</script>

