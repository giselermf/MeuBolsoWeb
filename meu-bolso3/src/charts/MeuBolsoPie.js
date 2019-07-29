import { Pie } from 'vue-chartjs'
import {
  getDataSetPie
} from "../util/Utils.js";

export default {
  extends: Pie,
  props: ['chartLabels', 'chartValues', 'positives', 'title'],
  data() {
    return {
      chartOptions: {
        responsive: false, maintainAspectRatio: false,
        title: {
          display: true
        },
        tooltips: {
          enabled: true,
          mode: 'single',
        },
        legend: { display: true, position:'right' },
        'onClick': this.graphClickEvent
      }
    }
  },
  watch: {
    chartValues: {
      handler(newData, oldData) {
        this.render();
      }
    }
  },
  methods: {
    render() {
      let dataset = getDataSetPie(this.chartLabels, this.chartValues);
      if (this._chart) this._chart.destroy();
      this.chartOptions.title.text = this.title;
      this.renderChart(dataset, this.chartOptions);
    },
    graphClickEvent(event, item) {
      this.$emit("drilldown-click", item[0]._index);
    }
  }
}
