<template>
<div id="app" class="ui vertical stripe segment">
    <div style="display: inline-grid;">
      <div>
        <p>Id : {{ category_id }}</p>
      </div>
      <div>
        <label class="form-label">Description:</label>
        <input v-model="description" placeholder="edit me" class="form-field"><br>
      </div>
      <div>
        <label class="form-label">Type:</label>
        <select class="form-field" v-model="selectedType" v-on:change="onChangeType" >
            <option v-for="type in getTypes()" v-bind:key="type" v-bind:value="type">
                {{ type }}
            </option>
        </select>
      </div>
      <div>
        <label class="form-label">Category:</label>
        <select class="form-field" v-model="selectedCategory" v-on:change="onChangeCategory">
            <option v-for="category in getCategories()" v-bind:key="category" v-bind:value="category">
                {{ category }}
            </option>
        </select>
      </div>
      <div>
        <label class="form-label">SubCategory:</label>
        <select class="form-field" v-model="selectedSubCategory">
            <option v-for="subcategory in getSubCategories()" v-bind:key="subcategory" v-bind:value="subcategory">
                {{ subcategory }}
            </option>
        </select>
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
import CategorySelectCombos from "./CategorySelectCombos.vue"
import { addFilterParam } from "../charts/ChartUtils.js";
import VueEvents from "vue-events";

export default {
  mixins : [CategorySelectCombos],
  components: { CategoryTable},
  data() {
    return {
      category_id: null,
      description: null
    };
  },
  mounted() {
    this.$events.$on("edit-record", eventData => this.onEdit(eventData));
    this.$events.$on("delete-record", eventData => this.onDelete(eventData));
  },
  methods: {
    onEdit: function(data) {
      this.description = data.Description;
      this.category_id = data.id;
      this.selectedType = data.Type;
      this.selectedCategory = data.Category;
      this.selectedSubCategory = data.SubCategory;
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
            type: this.selectedType,
            category: this.selectedCategory,
            subcategory: this.selectedSubCategory,
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
            type: this.selectedType,
            category: this.selectedCategory,
            subcategory: this.selectedSubCategory,
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
        category: this.selectedCategory,
        subcategory: this.selectedSubCategory,
        description: this.description,
        type: this.type
      };
      this.$events.fire("category-filter-set", addFilterParam(params));
    },
    reset: function() {
      this.category_id = null;
      this.selectedCategory = null;
      this.description = null;
      this.selectedType = null;
      this.selectedSubCategory = null;
      this.$events.fire("category-filter-reset");
    }
  }
};
</script>


<style
  src="../../static/meuBolso.css">

</style>