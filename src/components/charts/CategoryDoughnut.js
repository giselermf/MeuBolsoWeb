import { Pie } from 'vue-chartjs'

export default Pie.extend({
  data () {
    return {
      chartData: null,
      filters: null,
    }
  },
  watch: {
    chartData: function (newQuestion) {
      this.renderChart(this.chartData, {responsive: true, maintainAspectRatio: false});
    }
  },
  mounted () {
      this.getData();
      this.$events.$on('year-filter', eventData => this.onFilterSet(eventData))
      this.gradient = this.$refs.canvas.getContext('2d').createLinearGradient(0, 0, 0, 600)
      this.gradient.addColorStop(0, 'rgba(255, 0,0, 0.5)')
      this.gradient.addColorStop(0.5, 'rgba(255, 0, 0, 0.25)');
      this.gradient.addColorStop(1, 'rgba(255, 0, 0, 0)');      
  },
  methods: {
    udpdateData(response) {
      let results = response.data.data
      let labels = [];
      let values = [];
      for (let index in results) {
          let element = results[index];
          labels.push(element['Category']);
          values.push(Math.abs(element['Total']));
      }
      this.chartData = {
        labels: labels,
        datasets: [
          {
            label: 'Data One',
            borderColor: '#FC2525',
            pointBackgroundColor: 'white',
            borderWidth: 1,
            pointBorderColor: 'white',
            backgroundColor: this.gradient,
            data: values
          }
        ]
      }
    },
    getURL() {
        var url = 'http://127.0.0.1:5000/getAmountByCategory';
        if (this.filters != null) {
           url += '?filters='+this.filters
        }
        return url;
    },
    getData () {
      var axios = require('axios');
      var querystring = require('querystring');
      axios.get(this.getURL())
          .then((response) => {
              this.udpdateData(response);
          })
          .catch(function (error) {
              console.log(error);
          });
    },
    onFilterSet (filterText) {
      this.filters = filterText;
      this.getData();
      console.log('doughnuts', this.filters);
    },
  }
})
