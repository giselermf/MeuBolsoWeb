import { Pie } from 'vue-chartjs'
import {
  getDataSetPie
} from "./ChartUtils.js";

export default Pie.extend({
  props: ['chartLabels', 'chartValues', 'positives', 'title'],
  data() {
    return {
      chartOptions: {
        responsive: false, maintainAspectRatio: false,
        title: {
          display: true,
          text: this.title
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
        let dataset = getDataSetPie(this.chartLabels, this.chartValues);
        this.render(dataset);
      }
    }
  },
  methods: {
    render(dataset) {
      if (this._chart) this._chart.destroy();
      this.renderChart(dataset, this.chartOptions);
    },
    graphClickEvent(event, item) {
      this.$events.fire("drilldown-click", item[0]._index);
    }
  }
})
