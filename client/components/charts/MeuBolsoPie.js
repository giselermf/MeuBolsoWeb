import { Pie } from 'vue-chartjs'

export default Pie.extend({
  props: ['chartData'],
	data(){
		return{
      chartOptions: {responsive: false, maintainAspectRatio: false, legend: { display: false } }
    }
  },
  mounted () {
    this.renderChart(this.chartData, this.chartOptions);
  },
	watch:{
    'chartData': {
      handler (newData, oldData) {
        if (this._chart) this._chart.destroy();
        this.renderChart(this.chartData, this.chartOptions);
      }
    }
	},
})
