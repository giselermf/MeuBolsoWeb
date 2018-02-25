import { Bar } from 'vue-chartjs'
import {getChartData, getUrlFilters} from './ChartUtils.js'

export default Bar.extend({
  data () {
    return {
      year_filters: '',
      type_filters: '',
      category_filters: '',
      subcategory_filters: '',
      account_filters: '',
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
  props: ['url', 'xLabel', 'datasetLabel'],
  mounted () {
      this.getData();
      this.$events.$on('filter_year', eventData => this.onYearFilterSet(eventData));
      this.$events.$on('filter_type', eventData => this.onTypeFilterSet(eventData));
      this.$events.$on('filter_categories', eventData => this.onCategoryFilterSet(eventData));
      this.$events.$on('filter_subcategories', eventData => this.onSubcategoryFilterSet(eventData));
      this.$events.$on('filter_bankAccounts', eventData => this.onAccountFilterSet(eventData));      
  },
  methods: {
    getUrl() {
      return this.url + getUrlFilters(this.year_filters, this.type_filters, this.category_filters, this.subcategory_filters, this.account_filters);
    },
    udpdateData(response) {
      let chartData = getChartData(response.data.data, this.xLabel, this.datasetLabel )
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
    onAccountFilterSet (filterText) {
      this.account_filters = filterText;
      this.getData();
    },
  }
})
