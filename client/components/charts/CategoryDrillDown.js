import { Pie } from 'vue-chartjs'
import {
  groupDataBy,
  getDataSetPie
} from "./ChartUtils.js";

export default Pie.extend({
  props: ['allData', 'positives', 'title'],
  data() {
    return {
      typeSelected: null,
      categorySelected: null,
      drillDownLevel: 1,
      chartOptions: {
        responsive: false, maintainAspectRatio: false, legend: { display: false },
        title: {
          display: true,
          text: this.title
        },
        tooltips: {
          enabled: true,
          mode: 'single',
        },
        'onClick': this.graphClickEvent
      }
    }
  },
  mounted() {
    this.prepareData();
  },
  methods: {
    getParams() {
      let params = {};
      if (this.fromDate) params["fromDate"] = this.fromDate;
      if (this.toDate) params["toDate"] = this.toDate;
      return "?filter=" + JSON.stringify(params);
    },
    prepareData() {
      if (this.allData == null) return

      let groupedData;
      if (this.drillDownLevel == 1) {
        groupedData = groupDataBy(this.allData, "Type");
      } else if (this.drillDownLevel == 2) {
        let filterdData = this.allData.filter(element => element.Type == this.typeSelected);
        groupedData = groupDataBy(filterdData, "Category");
      } else if (this.drillDownLevel == 3) {
        let filterdData = this.allData.filter(element => element.Type == this.typeSelected && element.Category == this.categorySelected);
        groupedData = groupDataBy(filterdData, "SubCategory");
      }

      let values;
      if (this.positives) values = groupedData.values_positives
      else values = groupedData.values_negatives
      let dataset = getDataSetPie(groupedData.labels, values)
      this.render(dataset);
    },
    render(dataset) {
      if (this._chart) this._chart.destroy();
      this.chartOptions.title.text = this.getTitle();
      this.renderChart(dataset, this.chartOptions);
    },
    graphClickEvent(event, item) {
      let activeElement_index = item[0]._index;
      if (this.drillDownLevel == 1) {
        this.typeSelected = item[0]._chart.config.data.labels[activeElement_index];
        this.categorySelected = null;
      } else {
        this.categorySelected = item[0]._chart.config.data.labels[activeElement_index]
      }
      this.drillDownLevel = (this.drillDownLevel + 1) % 4;
      this.prepareData();
    },
    reset() {
      this.typeSelected = null;
      this.categorySelected = null;
      this.drillDownLevel = 1;
    },
    getTitle() {
      let title = this.title;
      if (this.typeSelected != null) title += " -> " + this.typeSelected;
      if (this.categorySelected != null) title += " -> " + this.categorySelected;
      return title;
    },
  },
  watch: {
    'allData': {
      handler(newData, oldData) {
        this.reset();
        this.prepareData();
      }
    }
  }
})
