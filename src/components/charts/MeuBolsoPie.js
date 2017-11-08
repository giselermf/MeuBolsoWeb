import { Pie } from 'vue-chartjs'
import { getUrlFilters} from './ChartUtils.js'

export default Pie.extend({
  data () {
    return {
      year_filters: '',
      type_filters: '',
      category_filters: '',
      subcategory_filters: '',
      account_filters: '',
      chartOptions: {responsive: false, maintainAspectRatio: false, legend: { display: false } }
    }
  },
  props: ['url', 'label'],
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
      let results = response.data.data
      let labels = [];
      let values = [];
      let colors = [];
      let backgroundCollors = ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"];
      for (let index in results) {
          let element = results[index];
          labels.push(element[this.label]);
          colors.push(backgroundCollors[values.length % backgroundCollors.length]);
          values.push( Math.abs(element['Total']));
      }
      let chartData = {
        labels: labels,
        datasets: [
          {
            label: 'Data One',
            pointBackgroundColor: 'white',
            borderWidth: 1, 
            pointBorderColor: 'white',
            backgroundColor: colors,
            data: values
          }
        ]
      };
      if (this._chart) this._chart.destroy();
      this.renderChart(chartData, this.chartOptions);
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
