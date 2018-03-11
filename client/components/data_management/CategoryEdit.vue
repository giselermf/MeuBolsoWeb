<template>
<div id="app" class="ui vertical stripe segment">
    <div style="display: inline-grid;">
      <div>
        <p>Id : {{ category_id }}</p>
      </div>
      <div>
        <label class="form-label">Type:</label>
        <input v-model="type" placeholder="edit me" class="form-field"> <br> 
      </div>
      <div>
        <label class="form-label">Category:</label>
        <input v-model="category" placeholder="edit me" class="form-field"> <br> 
      </div>
      <div>
        <label class="form-label">Subcategory:</label>
        <input v-model="subcategory" placeholder="edit me" class="form-field"> <br> 
      </div>
      <div>
        <label class="form-label">Description:</label>
        <input v-model="description" placeholder="edit me" class="form-field"><br>
      </div>
      <div style="display: flex;justify-content: center;padding-top: 1em"> 
          <button type="button" @click="save()" >Save</button>
          <button type="button" @click="add()" >Add</button>
          <button type="button" @click="search()" >Search</button>
          <button type="button" @click="reset()" >Reset</button>
      </div>
    </div>
    <category-table></category-table>

</div>
</template>

<script>
import CategoryTable from "./CategoryTable.vue";
import { addFilterParam } from "../charts/ChartUtils.js";
import VueEvents from "vue-events";

export default {
  components: { CategoryTable },
  data() {
    return {
      category_id: null,
      category: null,
      description: null,
      type: null,
      subcategory: null
    };
  },
  mounted() {
    this.$events.$on("edit-record", eventData => this.onEdit(eventData));
    this.$events.$on("delete-record", eventData => this.onDelete(eventData));
  },
  methods: {
    onEdit: function(data) {
      this.category_id = data.id;
      this.category = data.category;
      this.description = data.description;
      this.type = data.type;
      this.subcategory = data.subcategory;
    },
    onDelete: function(data) {
      var axios = require("axios");
      var querystring = require("querystring");
      axios
        .delete(
          "http://127.0.0.1:5000/categories/" + data.id,
          querystring.stringify()
        )
        .then(response => {
          this.$events.fire("category-filter-reset");
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    save: function() {
      var axios = require("axios");
      var querystring = require("querystring");
      axios
        .post(
          "http://127.0.0.1:5000/categories/",
          querystring.stringify({
            id: this.category_id,
            type: this.type,
            category: this.category,
            subcategory: this.subcategory,
            description: this.description
          })
        )
        .then(response => {
          this.$events.fire("category-filter-reset");
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    add: function() {
      var axios = require("axios");
      var querystring = require("querystring");
      axios
        .post(
          "http://127.0.0.1:5000/categories/",
          querystring.stringify({
            id: null,
            type: this.type,
            category: this.category,
            subcategory: this.subcategory,
            description: this.description
          })
        )
        .then(response => {
          this.$events.fire("category-filter-reset");
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    search: function() {
      let params = {
        category: this.category,
        subcategory: this.subcategory,
        description: this.description,
        type: this.type
      };
      this.$events.fire("category-filter-set", addFilterParam(params));
    },
    reset: function() {
      this.category_id = null;
      this.category = null;
      this.description = null;
      this.type = null;
      this.subcategory = null;
      this.$events.fire("category-filter-reset");
    }
  }
};
</script>


<style
  src="../../static/meuBolso.css">

</style>