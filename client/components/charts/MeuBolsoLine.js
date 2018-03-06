import { Line } from 'vue-chartjs'

export default Line.extend({
  data () {
    return {
      options: {
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
