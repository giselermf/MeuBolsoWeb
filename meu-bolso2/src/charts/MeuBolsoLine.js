import { Line } from 'vue-chartjs'

export default {
  extends: Line,
  props: ['chartData', 'title'],
  data() {
    return {
      options: {
        title: {
          display: true,
          text: this.title
        },
        legend: {
          display: true
        },
        showLines: true,
        responsive: false,
        maintainAspectRatio: false
      }
    }
  },
  mounted() {
    this.renderChart(this.chartData, this.options)
  },
  watch: {
    'chartData': {
      handler(newData, oldData) {
        if (this._chart) this._chart.destroy();
        this.renderChart(this.chartData, this.options);
      }
    }
  }
}
