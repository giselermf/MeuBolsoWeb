<template>
  <div>
    <canvas ref="canvas" width="0" height="0"></canvas>
    <div class="tile is-ancestor">
      <div>
        <multiselect v-model="value" :options="options" :multiple="true" :close-on-select="true" :clear-on-select="false" 
        :hide-selected="true" :preserve-search="true" selectLabel=""  placeholder="All Categories" label="Category" track-by="Category"
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
      options: []
    }
  },
   mounted() {
    var axios = require('axios');
        var querystring = require('querystring');
        axios.get('http://127.0.0.1:5000/getDistinctCategories', querystring.stringify())
          .then((response) => {
            this.options = response.data.filter_categories;
          })
          .catch(function (error) {
            console.log(error);
          });
  },
  methods: {
    updateHandler(data) {
        var filters = '';
        this.value.forEach(function(element) { 
          filters += ",'" + element.Category + "'";
        }, this);
        this.$events.fire('category-filter', filters.substring(1));
      }
  }
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>