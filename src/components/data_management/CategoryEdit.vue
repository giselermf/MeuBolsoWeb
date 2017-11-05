<template>
<div id="app" class="ui vertical stripe segment">
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
          <button type="button" @click="save()" >Save</button>
          <button type="button" @click="add()" >Add</button>
      </div>
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
    mounted () {
      this.$events.$on('edit-record', eventData => this.onEdit(eventData))
      this.$events.$on('delete-record', eventData => this.onDelete(eventData))
    },
    methods: {
        onEdit: function(data) {
          this.category_id = data.id
          this.category = data.category
          this.description = data.description 
        },
        onDelete: function(data) {
          this.category_id = data.id
          this.category = data.category
          this.description = data.description 
          var axios = require('axios');
          var querystring = require('querystring');
          axios.delete('http://127.0.0.1:5000/categories/'+this.category_id, querystring.stringify())
            .then((response) => {
              this.$events.fire('filter-reset')
            })
            .catch(function (error) {
              console.log(error);
            });
        },
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
        },
        add: function() {
          var axios = require('axios');
          var querystring = require('querystring');
          axios.post('http://127.0.0.1:5000/categories/', querystring.stringify({ 
              id: null,
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


<style
  src="../../../static/meuBolso.css">
</style>