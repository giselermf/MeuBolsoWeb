import { Doughnut } from 'vue-chartjs'

export default Doughnut.extend({
  data () {
    return {
      chartData: null
    }
  },
 // created () {
 //   this.getData();
 // },
  watch: {
    chartData: function (newQuestion) {
      this.renderChart(this.chartData, {responsive: true, maintainAspectRatio: false});
    }
  },
  mounted () {
      this.getData();
      this.gradient = this.$refs.canvas.getContext('2d').createLinearGradient(0, 0, 0, 450)
      this.gradient.addColorStop(0, 'rgba(255, 0,0, 0.5)')
      this.gradient.addColorStop(0.5, 'rgba(255, 0, 0, 0.25)');
      this.gradient.addColorStop(1, 'rgba(255, 0, 0, 0)');      
  },
  methods: {
    getData () {
      var axios = require('axios');
      var querystring = require('querystring');
      axios.get('http://127.0.0.1:5000/getExpensesByMonth')
          .then((response) => {
              let results = response.data.data
              let labels = [];
              let values = [];
              for (let index in results) {
                  let element = results[index];
                  labels.push(element['Category']);
                  values.push(Math.abs(element['Total']));
              }
              this.chartData = {
                labels: labels, // ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
                datasets: [
                  {
                    label: 'Data One',
                    borderColor: '#FC2525',
                    pointBackgroundColor: 'white',
                    borderWidth: 1,
                    pointBorderColor: 'white',
                    backgroundColor: this.gradient,
                    data: values // [40, 39, 10, 40, 39, 80, 40]
                  }
                ]
              }
          })
          .catch(function (error) {
              console.log(error);
          });
    }
  }
})
