import { Line } from 'vue-chartjs'

export default Line.extend({
  props: ['chartData', 'title'],
  mounted () {
    if (this._chart) this._chart.destroy();
    this.renderChart(this.chartData, this.options )
  },
  watch:{
    'chartData': {
      handler (newData, oldData) {
        console.log('watching data from line')
        if (this._chart) this._chart.destroy();
        this.renderChart(this.chartData, this.options);
      }
    }
	},
  data () {
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
          responsive: true,
          maintainAspectRatio: false
        }
    }
  }
})
