import { Line } from 'vue-chartjs'

export default Line.extend({
  data () {
    return {
      year_filters: '',
      type_filters: '',
      category_filters: '',
      subcategory_filters: '',
      options: {
        legend: {
          display: true
        },
        responsive: true,
        maintainAspectRatio: false
      }
    }
  },
  props: ['url', 'xLabel', 'datasetLabel'],
  mounted () {
      this.getData();
      this.$events.$on('year-filter', eventData => this.onYearFilterSet(eventData));
      this.$events.$on('type-filter', eventData => this.onTypeFilterSet(eventData));
      this.$events.$on('category-filter', eventData => this.onCategoryFilterSet(eventData));
      this.$events.$on('subcategory-filter', eventData => this.onSubcategoryFilterSet(eventData)); 
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

      let labels = [new Set(response.data.data.map(item => item[this.xLabel]))];
      //sort if Date
      labels = Array.from(labels[0]).sort(function(a,b) {
          a = a.split('/').reverse().join('');
          b = b.split('/').reverse().join('');
          return a > b ? 1 : a < b ? -1 : 0;
        });

      let datasetLabels = [new Set(response.data.data.map(item => item[this.datasetLabel]))];
      datasetLabels = Array.from(datasetLabels[0]);

      datasetLabels.forEach(function(aDataset) { 
        values = [];
        labels.forEach(function(oneLabel){
            let filterMap = {};
            filterMap[this.datasetLabel] = aDataset
            filterMap[this.xLabel] = oneLabel
            let result = this.filter(response.data.data, filterMap)
            let total = 0;
            if (result[0] != undefined) {
               total = result[0]['Total'];  
            } 
            values.push(total);
            
          }, this);
          datasets.push(
            {
              label: aDataset,
              borderWidth: 1,
              backgroundColor: backgroundCollors[datasets.length % backgroundCollors.length],
              data: values
            });
                
      }, this); 
      let chartData = {
        labels: labels,
        datasets: datasets
      };
      if (this._chart) this._chart.destroy();
      this.renderChart(chartData, this.options )
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
