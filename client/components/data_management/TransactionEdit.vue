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
        <input v-model="type" placeholder="edit me" class="form-field"> <br> 
      </div>
      <div>
        <label class="form-label">Category:</label>
        <input v-model="category" placeholder="edit me" class="form-field"> <br> 
      </div>
      <div>
        <label class="form-label">SubCategory:</label>
        <input v-model="SubCategory" placeholder="edit me" class="form-field"><br>
      </div>
      <div style="display: flex;justify-content: center;padding-top: 1em"> 
          <button type="button" @click="save()" >Save</button>
      </div>
    </div> 
</div>
</template>

<script>
export default {
  data() {
    return {
      category_id: null,
      type: null,
      category: null,
      SubCategory: null,
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
      this.category = data.Category;
      this.SubCategory = data.SubCategory;
      this.bank = data.BankName;
      this.description = data.Description;
      this.type = data.Type;
    },
    save: function() {
      var axios = require("axios");
      var querystring = require("querystring");
      axios
        .post(
          "http://127.0.0.1:5000/transactions/",
          querystring.stringify({
            id: this.category_id,
            category: this.category,
            SubCategory: this.SubCategory,
            Type: this.type
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


<style
  src="../../static/meuBolso.css">

</style>