<template>
  <div id="app" class="ui horizontal segments">
    <div class="ui  segment eight wide column" >
       
       <div class="field is-horizontal" >
            <div class="field-label">
                <label class="label">Id</label>
            </div>
            <div class="field-body">
                <div class="field is-grouped">
                  <label> {{ category_id }} </label>
                </div>
            </div>
        </div>


         <div class="field is-horizontal" >
            <div class="field-label">
                <label class="label">Description</label>
            </div>
            <div class="field-body">
                <div class="field is-grouped">
                  <input class="control input" v-model="description" placeholder="edit me"/> 
                </div>
            </div>
        </div>


        <category-select-combos ref="typecombos"></category-select-combos>

        <div class="field is-grouped is-grouped-centered" style="padding-top: 10px;" >
            <p class="control">
              <button class="button is-link" type="button" @click="save()" >Save</button>
            </p>
            <p class="control">
              <button class="button is-link" type="button" @click="add()" >Add</button>
            </p>
        </div>

        <div class="field is-grouped is-grouped-centered">
            <p class="control">
              <button class="button is-link" type="button" @click="search()" >Search</button>
            </p>
            <p class="control">
              <button class="button is-link" type="button" @click="reset()" >Reset</button>
            </p>
        </div>
    </div>

  
    <div class="ui  segment four wide column" >
      <category-table></category-table>
    </div>  
  </div>
</template>

<script>
import CategoryTable from "./CategoryTable.vue";
import CategorySelectCombos from "../util/CategorySelectCombos.vue"
import { addFilterParam } from "../util/Utils.js";
import VueEvents from "vue-events";
import {HTTP} from '../util/http-common';

export default {
  components: { CategoryTable, CategorySelectCombos},
  data() {
    return {
      category_id: null,
      description: null,
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
      this.$refs.typecombos.setValues(data.category.Type, data.category.Category, data.category.SubCategory);
    },
    onDelete: function(data) {
      HTTP.delete(
          "categories/" + data.id,
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
      if (this.$refs.typecombos.getSelectedCategoryId() == null) return;
      HTTP
        .post(
          "categories/",
          querystring.stringify({
            id : this.category_id,
            selectedCategoryid : this.$refs.typecombos.getSelectedCategoryId(),
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
      console.log('on add', this.description, this.$refs.typecombos.getSelectedCategoryId());
      if (this.$refs.typecombos.getSelectedCategoryId() == null) return;
      HTTP
        .post(
          "categories/",
          querystring.stringify({
            id: null,
            selectedCategoryid : this.$refs.typecombos.getSelectedCategoryId(),
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
        category: this.$refs.typecombos.getSelectedCategory(),
        subcategory: this.$refs.typecombos.getSelectedSubCategory(),
        description: this.description,
        type: this.$refs.typecombos.getSelectedType()
      };
      this.$events.fire("category-filter-set", addFilterParam(params));
    },
    reset: function() {
      this.id = null;
      this.description = null;
      this.$refs.typecombos.resetValues();
      this.$events.fire("category-filter-reset");
    }
  }
};
</script>