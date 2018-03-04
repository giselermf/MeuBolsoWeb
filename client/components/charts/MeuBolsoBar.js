import { Bar } from 'vue-chartjs'

export default Bar.extend({
  data () {
    return {
      options: {
        scales: {
          yAxes: [{
            stacked: true
          }],
          xAxes: [ {
            stacked: true,
            categoryPercentage: 0.5,
            barPercentage: 1
          }]
        },
        legend: {
          display: false
        },
        responsive: true,
        maintainAspectRatio: false
      }
    }
  },
  props: ['chartData'],
  mounted () {
    if (this._chart) this._chart.destroy();
    this.renderChart(this.chartData, this.options )
  },
  watch:{
    'chartData': {
      handler (newData, oldData) {
        if (this._chart) this._chart.destroy();
        this.renderChart(this.chartData, this.options);
      }
    }
	},
})
