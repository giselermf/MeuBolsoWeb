<template>
<div>
    <p><a v-on:click="setIncomes"> Incomes </a> <a v-on:click="setExpenses"> Expenses </a></p>
    <meu-bolso-pie :width="500" :height="200" 
    :chartLabels="chartLabels" :chartValues="chartValues" :title="compositeTitle" :positives="isPositive" ></meu-bolso-pie>
    <br>
    <vuetable
        :data="tableData"
        :api-mode=false
        table-wrapper="#content"
        :fields="['Group', 'Value']"
    ></vuetable>      
</div>
</template>

<script>
import MeuBolsoPie from "../charts/MeuBolsoPie.js";
import Vuetable from "vuetable-2/src/components/Vuetable.vue";
import { groupDataBy } from "../charts/ChartUtils.js";

export default {
  components: {
    Vuetable,
    MeuBolsoPie
  },
  props: ["allData"],
  data() {
    return {
      compositeTitle: null,
      currentCategoryType: 'Expenses',
      labels: [],
      values: [],
      tableData: [],
      chartLabels: null,
      chartValues: null,
      drillDownLevel: 1,
    };
  },
  mounted() {
    this.$events.$on("drilldown-click", eventData => this.onClick(eventData));
  },
  watch: {
    allData: {
      handler(newData, oldData) {
        this.prepareData();
      }
    }
  },
  methods: {
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
      console.log("on click",this.chartLabels, event, this.typeSelected, this.categorySelected);
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
    setIncomes() {
      this.currentCategoryType = "Incomes";
      this.reset();
    },
    setExpenses() {
      this.currentCategoryType = 'Expenses';
      this.reset();
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