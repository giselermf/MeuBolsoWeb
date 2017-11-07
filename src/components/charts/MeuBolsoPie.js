import { Pie } from 'vue-chartjs'

export default Pie.extend({
  data () {
    return {
      year_filters: '',
      type_filters: '',
      category_filters: '',
      subcategory_filters: '',
    }
  },
  props: ['url', 'label'],
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
      this.renderChart(chartData, {responsive: true, maintainAspectRatio: false, legend: { display: false } });
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
