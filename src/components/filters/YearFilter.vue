<template>
  <div>
    <canvas ref="canvas" width="0" height="0"></canvas>
    <div class="tile is-ancestor">
      <div>
        <multiselect v-model="value" :options="options" :multiple="true" :close-on-select="true" :clear-on-select="false" 
        :hide-selected="true" :preserve-search="true" selectLabel="" placeholder="All years" label="Year" track-by="Year" 
        @input="updateHandler">
        </multiselect>
      </div>
    </div>
  </div>
</template>

<script>
import Multiselect from 'vue-multiselect'
import axios from 'axios';

export default {
  components: {
    Multiselect
  },
  data () {
    return {
      value: [],
      options: [],
      year_filters: '',
      type_filters: '',
      category_filters: '',
      subcategory_filters: ''
    }
  },
  mounted() {
      this.$events.$on('year-filter', eventData => this.onYearFilterSet(eventData));
      this.$events.$on('type-filter', eventData => this.onTypeFilterSet(eventData));
      this.$events.$on('category-filter', eventData => this.onCategoryFilterSet(eventData));
      this.$events.$on('subcategory-filter', eventData => this.onSubcategoryFilterSet(eventData));
      this.getData();
  },
  methods: {
    getData() {
      var axios = require('axios');
      var querystring = require('querystring');
      axios.get(this.getUrl(), querystring.stringify())
        .then((response) => {
          this.options = response.data.filter_year;
          console.log(this.options);
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    updateHandler(data) {
      var filters = '';
      this.value.forEach(function(element) {
        filters += "," + element.Year
      }, this);
      this.$events.fire('year-filter', filters.substring(1));
    },
    getUrl() {
      var url = 'http://127.0.0.1:5000/getDistinctYears?';
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
    } 
  }
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>