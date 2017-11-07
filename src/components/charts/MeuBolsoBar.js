import { Bar } from 'vue-chartjs'

export default Bar.extend({
  data () {
    return {
      chartData: null,
      year_filters: '',
      type_filters: '',
      category_filters: '',
      subcategory_filters: ''
    }
  },
  props: ['url', 'label'],
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
    getUrl() {
      var url = this.url;
      if (this.year_filters != null && this.year_filters != '')
        url += '&year_filter='+this.year_filters;
      if (this.type_filters != null && this.type_filters != '') 
        url += '&type_filter='+this.type_filters;
      if (this.category_filters != null && this.category_filters != '')
        url += '&category_filter='+this.category_filters;
      if (this.subcategory_filters != null && this.subcategory_filters != '')
        url += '&subcategory_filter='+this.subcategory_filters;
      return url;
    },
    filter(arr, criteria) {
      return arr.filter(function(obj) {
        return Object.keys(criteria).every(function(c) {
          return obj[c] == criteria[c];
        });
      });
    },
    udpdateData(response) {
      let datasets = [];
      let values = [];
      let backgroundCollors = ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"];

      let labels = [new Set(response.data.data.map(item => item.yearmonth))];
      labels = Array.from(labels[0]);
      let uniqueSubCategories = [new Set(response.data.data.map(item => item.SubCategory))];
      uniqueSubCategories = Array.from(uniqueSubCategories[0]);

      uniqueSubCategories.forEach(function(uniqueElement) { 
        values = [];
        labels.forEach(function(oneLabel){
            let result = this.filter(response.data.data, {SubCategory: uniqueElement, yearmonth: oneLabel})
            let total = 0;
            if (result[0] != undefined) {
               total = Math.abs(result[0]['Total']);  
            } 
            values.push(total);
            
          }, this);
          datasets.push(
            {
              label: uniqueElement,
              borderWidth: 1,
              backgroundColor: backgroundCollors[datasets.length % backgroundCollors.length],
              data: values
            });
                
      }, this);

      this.chartData = {
        labels: labels,
        datasets: datasets,
      /*  options: {
          scales: {
            xAxes: [{ 
              stacked: true, 
              gridLines: { display: false },
              }],
            yAxes: [{ 
              stacked: true, 
              ticks: {
                callback: function(value) { return value; },
               }, 
              }],
          } // scales
        } */
      }
    },
    getData () {
      var axios = require('axios');
      var querystring = require('querystring');
      axios.get(this.getUrl())
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
