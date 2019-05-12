import { Bar } from 'vue-chartjs'

export default {
  extends: Bar,
  data() {
    return {
      options: {
        scales: {
          yAxes: [{
            stacked: true,
            ticks: {
              beginAtZero: true
            },
            gridLines: {
              display: true
            }
          }],
          xAxes: [{
            stacked: true,
            categoryPercentage: 0.5,
            barPercentage: 1,
            gridLines: {
              display: false
            }
          }]
        },
        title: {
          display: true,
          text: this.title
        },
        legend: {
          display: true
        },
        responsive: true,
        maintainAspectRatio: false
      }
    }
  },
  props: ['chartData', 'title'],
  mounted() {
    if (this._chart) this._chart.destroy();
    this.renderChart(this.chartData, this.options);
  },
  watch: {
    'chartData': {
      handler(newData, oldData) {
        this.options.title.text = this.title;
        if (this._chart) this._chart.destroy();
        this.renderChart(this.chartData, this.options);
      }
    }
  },
}
