<template>
  <div>
    <meu-bolso-bar
      :height="height"
      :chartData="chartData"
      xLabel="yearmonth"
      data-set-label="grouper"
      :title="title"
    ></meu-bolso-bar>
    <v-checkbox v-model="showTable" :label="`Show table: ${showTable.toString()}`"></v-checkbox>
    <div v-if="showTable && tableData.length>0" class="ui segment">
      <v-data-table ref="vuetableData" :headers="tableLabels" :items="tableData" class="elevation-1">
        <template slot="items" slot-scope="props">
          <td v-for="header in tableLabels" :key="header.value">{{ props.item[header.text] }}</td>
        </template>
      </v-data-table>
    </div>
  </div>
</template> 

<script>
import meuBolsoBar from "../charts/MeuBolsoBar.js";
import {
  getGroupByMonthAnd,
  getLabelAndDatabaseBar,
  colors
} from "../util/Utils.js";

export default {
  components: {
    meuBolsoBar
  },
  props: ["allData", "height", "grouper"],
  data() {
    return {
      showTable: true,
      title: this.grouper + " Over Months",
      tableData: [],
      chartData: {},
      tableLabels: [{ text: "name", value: "name" }]
    };
  },
  watch: {
    allData: {
      handler(newData, oldData) {
        console.log('!!! allData')
        this.getChartData();
      }
    },
    grouper: {
      handler(newData, oldData) {
        this.title = this.grouper + " Over Months";
        console.log('!!! grouper')

        this.getChartData();
      }
    }
  },
  mounted() {
    console.log('!!! created')
    this.getChartData();
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
    getChartData() {
      if (this.allData == null) return;
      let rows = {};
      let groupedData = getGroupByMonthAnd(this.allData, this.grouper);
      let newData = [];
      //clean table data
      this.tableData.splice(0, this.tableData.length);

      for (let col in groupedData) {
        for (let desc in groupedData[col]) {
          if (groupedData[col][desc] != 0) {
            let entry = {};
            entry["name"] = desc;
            entry["date"] = col;
            entry["value"] = groupedData[col][desc];
            newData.push(entry);
          }
        }
      }
      let result = newData.reduce(function(r, a) {
        r[a["name"]] = r[a["name"]] || [];
        r[a["name"]].push(a);
        return r;
      }, Object.create(null));

      for (let col in result) {
        let entry = {};
        entry["name"] = col;
        for (let value in result[col]) {
          let date = result[col][value]["date"];
          let newLabel = { text: date, value: date };
          if (this.tableLabels.findIndex(x => x.text == date) === -1) {
            this.tableLabels.push(newLabel);
          }
          entry[date] = result[col][value]["value"];
        }
        this.tableData.push(entry);
      }
      this.chartData = getLabelAndDatabaseBar(groupedData, colors);
    }
  }
};
</script>

