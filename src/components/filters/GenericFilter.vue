<template>
    <div>
      <multiselect v-model="value" :options="options" :multiple="true" :close-on-select="true" :clear-on-select="false" 
      :hide-selected="true" :preserve-search="true" selectLabel="" :placeholder="placeholder" :label="label" :track-by="trackBy"
      @input="updateHandler">
      </multiselect>
    </div>
</template>

<script>
import Multiselect from 'vue-multiselect'
import axios from 'axios';
import {getUrlFilters} from '../charts/ChartUtils.js'
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
      subcategory_filters: '',
      account_filters: '',
      url: null,
      placeholder:null,
      label:null,
      trackBy:null,
      filterName: null
    }
  },
  mounted() {
      this.$events.$on('filter_year', eventData => this.onYearFilterSet(eventData));
      this.$events.$on('filter_type', eventData => this.onTypeFilterSet(eventData));
      this.$events.$on('filter_categories', eventData => this.onCategoryFilterSet(eventData));
      this.$events.$on('filter_subcategories', eventData => this.onSubcategoryFilterSet(eventData));
      this.$events.$on('filter_bankAccounts', eventData => this.onAccountFilterSet(eventData));
      this.getData();
  },
  methods: {
    getData() {
      var axios = require('axios');
      var querystring = require('querystring');
      axios.get(this.getUrl(), querystring.stringify())
        .then((response) => {
          this.options = response.data[this.filterName];
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    updateHandler(data) {
      var filters = '';
      this.value.forEach(function(element) {
        filters += ",\"" + element[this.trackBy] + "\"";
      }, this);
      this.$events.fire(this.filterName, filters.substring(1));
    },
    getUrl() {
      return this.url + getUrlFilters(this.year_filters, this.type_filters, this.category_filters, this.subcategory_filters, this.account_filters)
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
    } 
  }
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>