import { Pie } from 'vue-chartjs'

export default Pie.extend({
  data () {
    return {
      url: null,
      chartData: null,
      year_filters: null,
      type_filters: null,
      category_filters: null,
      subcategory_filters: null,
    }
  },
  
  watch: {
    chartData: function (newQuestion) {
      this.renderChart(this.chartData, {responsive: true, maintainAspectRatio: false});
    }
  },
  mounted () {
      this.getData();
      this.$events.$on('year-filter', eventData => this.onYearFilterSet(eventData))
      this.$events.$on('type-filter', eventData => this.onTypeFilterSet(eventData))
      this.$events.$on('category-filter', eventData => this.onCategoryFilterSet(eventData))
      this.$events.$on('subcategory-filter', eventData => this.onSubcategoryFilterSet(eventData))
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
        var url = 'http://127.0.0.1:5000/getAmountByCategory?';
        if (this.year_filters != null && this.year_filters != '') {
           url += '&year_filter='+this.year_filters
        }
        if (this.type_filters != null && this.type_filters != '') {
          url += '&type_filter='+this.type_filters
        }
        if (this.category_filters != null && this.category_filters != '') {
          url += '&category_filter='+this.category_filters
        }
        if (this.subcategory_filters != null && this.subcategory_filters != '') {
          url += '&subcategory_filter='+this.subcategory_filters
        }
        console.log(url);
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
    onYearFilterSet (filterText) {
      this.year_filters = filterText;
      this.getData();
    },
    onTypeFilterSet (filterText) {
      this.type_filters = filterText;
      this.getData();
    },
    onCategoryFilterSet (filterText) {
      this.category_filters = filterText;
      this.getData();
    },
    onSubcategoryFilterSet (filterText) {
      this.subcategory_filters = filterText;
      this.getData();
    },
  }
})
