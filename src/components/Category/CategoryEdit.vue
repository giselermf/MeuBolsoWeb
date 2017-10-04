<template>
    <div style="display: inline-grid;">
      <div>
        <p>Id : {{ category_id }}</p>
      </div>
      <div>
        <label class="form-label">Category:</label>
        <input v-model="category" placeholder="edit me" class="form-field"> <br> 
      </div>
      <div>
        <label class="form-label">Description:</label>
        <input v-model="description" placeholder="edit me" class="form-field"><br>
      </div>
      <div style="display: flex;justify-content: center;padding-top: 1em"> 
          <button type="button" @click="save()" >Save/Add</button>
      </div>
    </div> 
</template>

<script>
  export default {
    props: ['category_id', 'category', 'description'],
    data() {
      return {
        status: null,
      };
    },
    methods: {
        save: function() {
          var axios = require('axios');
          var querystring = require('querystring');
          axios.post('http://127.0.0.1:5000/categories/', querystring.stringify({ 
              id: this.category_id,
              category: this.category,
              description: this.description}))
            .then((response) => {
              this.$events.fire('filter-reset')
            })
            .catch(function (error) {
              console.log(error);
            });
        }
      }
  }
</script>