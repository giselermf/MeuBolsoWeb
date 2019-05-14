<template>
  <div>
    <select v-model="currentCategoryType" @change="reset()">
      <option>Incomes</option>
      <option>Expenses</option>
    </select>
    <meu-bolso-pie
      :width="500"
      :height="200"
      @drilldown-click="onClick"
      :chartLabels="chartLabels"
      :chartValues="chartValues"
      :title="compositeTitle"
      :positives="isPositive"
    ></meu-bolso-pie>
    <br>
    <v-flex xs12 sm6 md6>
      <v-data-table
        :headers="tableHeaders"
        :items="tableData"
        class="elevation-1 .theme--light"
        hide-actions
        hide-headers
      >
        <template v-slot:items="props">
          <td class="text-xs-right">{{ props.item.Group }}</td>
          <td class="text-xs-right">{{ props.item.Value }}</td>
        </template>
      </v-data-table>
    </v-flex>
  </div>
</template>

<script>
import MeuBolsoPie from "./MeuBolsoPie.js";
import { groupDataBy } from "../util/Utils.js";

export default {
  components: {
    MeuBolsoPie
  },
  props: ["allData"],
  data() {
    return {
      compositeTitle: null,
      currentCategoryType: "Expenses",
      labels: [],
      values: [],
      tableData: [],
      chartLabels: null,
      chartValues: null,
      drillDownLevel: 1,
      tableHeaders: [
        { value: "Group", text: "Group" },
        { value: "Value", text: "Value" }
      ]
    };
  },
  watch: {
    allData: {
      handler(newData, oldData) {
        this.prepareData();
      }
    }
  },
  methods: {
    formatValues(value) {
      if (value == 0 || value == null) return "";
      if (!this.isPositive())
        return '<div style="text-align: end;color: red;">' + value + "</span>";
      else
        return (
          '<div style="text-align: end;color: black;">' + value + "</span>"
        );
    },
    prepareData() {
      this.groupData();
      this.prepareTableData();
      this.prepareChartData();
    },
    groupData() {
      if (this.allData == null) return;
      let groupedData;
      if (this.drillDownLevel == 1) {
        groupedData = groupDataBy(this.allData, "Type");
      } else if (this.drillDownLevel == 2) {
        let filterdData = this.allData.filter(
          element => element.Type == this.typeSelected
        );
        groupedData = groupDataBy(filterdData, "Category");
      } else if (this.drillDownLevel == 3) {
        let filterdData = this.allData.filter(
          element =>
            element.Type == this.typeSelected &&
            element.Category == this.categorySelected
        );
        groupedData = groupDataBy(filterdData, "SubCategory");
      }
      let values;
      if (groupedData != undefined) {
        if (this.isPositive()) values = groupedData.values_positives;
        else values = groupedData.values_negatives;
        this.labels = groupedData.labels;
        this.values = values;
      }
    },
    prepareChartData() {
      this.chartLabels = this.tableData.map(x => x.Group);
      this.chartValues = this.tableData.map(x => x.Value);
      this.compositeTitle = this.getTitle();
    },
    prepareTableData() {
      //clean table
      this.tableData.splice(0, this.tableData.length);
      for (let x in this.values) {
        if (this.values[x] != undefined) {
          let oneEntry = { Group: this.labels[x], Value: this.values[x] };
          this.tableData.push(oneEntry);
        }
      }
    },
    onClick(event) {
      if (this.drillDownLevel == 1) {
        this.typeSelected = this.chartLabels[event];
        this.categorySelected = null;
      } else if (this.drillDownLevel == 2) {
        this.categorySelected = this.chartLabels[event];
      } else if (this.drillDownLevel == 3) {
        return;
      }
      this.drillDownLevel = (this.drillDownLevel + 1) % 4;
      this.prepareData();
    },
    getTitle() {
      let title = this.currentCategoryType;
      if (this.typeSelected != null) title += " -> " + this.typeSelected;
      if (this.categorySelected != null)
        title += " -> " + this.categorySelected;
      return title;
    },
    isPositive() {
      return this.currentCategoryType == "Incomes";
    },
    reset() {
      this.drillDownLevel = 1;
      this.typeSelected = null;
      this.categorySelected = null;
      this.prepareData();
    }
  }
};
</script>