<template>
<div id="app" class="ui vertical stripe segment">
    <div style="display: inline-grid;">
      <div >
        <p class="read-only-form-field">Id : {{ category_id }}</p>
      </div>
      <div >
        <p class="read-only-form-field">Description : {{ description }}</p>
      </div>
      <div>
        <p class="read-only-form-field"> Bank : {{ bank }}</p>
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
      </div>
    </div> 
</div>
</template>

<script>
import CategorySelectCombos from "../util/CategorySelectCombos.vue"

export default {
  mixins : [CategorySelectCombos],
  data() {
    return {
      category_id: null,
      type_data: null,
      category_data: null,
      description: null,
      bank: null
    };
  },
  mounted() {
    this.$events.$on("edit-record", eventData => this.onEdit(eventData));
  },
  methods: {
    onEdit: function(data) {
      this.category_id = data.id;
      this.bank = data.BankName;
      this.description = data.Description;
      this.selectedType = data.Type;
      this.selectedCategory = data.Category;
      this.selectedSubCategory = data.SubCategory;
    },
    save: function() {
      var axios = require("axios");
      var querystring = require("querystring");
      axios
        .post(
          "http://127.0.0.1:5000/transactions/",
          querystring.stringify({
            id: this.category_id,
            category: this.selectedSubCategory,
            SubCategory: this.selectedSubCategory,
            Type: this.selectedType
          })
        )
        .then(response => {
          this.$events.fire("filter-reset");
        })
        .catch(function(error) {
          console.log(error);
        });
    }
  }
};
</script>