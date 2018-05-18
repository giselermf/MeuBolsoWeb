<template>
<div id="app" class="ui vertical stripe segment">
    <div style="display: inline-grid;">
      <div >
        <p class="read-only-form-field">Description : {{ description }}</p>
      </div>
      <div>
        <p class="read-only-form-field"> Bank : {{ bank }}</p>
      </div>  
      <category-select-combos ref="search_typecombos" ></category-select-combos>
      <div style="display: flex;justify-content: center;padding-top: 1em"> 
          <button type="button" @click="save()" >Save</button>
      </div>
    </div> 
</div>
</template>

<script>
import CategorySelectCombos from "../util/CategorySelectCombos.vue"

export default {
  components: {CategorySelectCombos},
  data() {
    return {
      transaction_id: null,
      description: null,
      bank: null
    };
  },
  mounted() {
    this.$events.$on("edit-record", eventData => this.onEdit(eventData));
  },
  methods: {
    onEdit: function(data) {
      this.transaction_id = data.id;
      this.bank = data.BankName;
      this.description = data.Description;
      this.$refs.search_typecombos.selectedType = data.Type;
      this.$refs.search_typecombos.selectedCategory = data.Category;
      this.$refs.search_typecombos.selectedSubCategory = data.SubCategory;
    },
    save: function() {
      var axios = require("axios");
      var querystring = require("querystring");
      axios
        .post(
          "http://127.0.0.1:5000/transactions/",
          querystring.stringify({
            transaction_id: this.transaction_id,
            category_id: this.$refs.search_typecombos.getSelectedCategoryId()
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