<template>
    <div>
      <div class="field is-horizontal-left" >
          <div class="field-body">
              <div class="field is-grouped">
                  <p class="control is-expanded">
                          <input type="text" class="input" v-model="folder" placeholder="source of bank files"> <br> 
                  </p>
                  <p class="control">
                      <button class="button is-link" v-on:click="processData">Process Data</button>
                  </p>
          </div></div>
      </div>
    </div>
</template>

<script>
export default {
    components: {

    },
    data: function () {
        return {
            url: "http://127.0.0.1:5000/processData/",
            folder: "/Users/gisele/Documents/bankFiles/"
        }
    },
    methods: {
        processData() {
            console.log('processing');
            var axios = require('axios');
            var querystring = require('querystring');
            axios.get(this.url+"?folder= \"" +this.folder + "\"", querystring.stringify())
                .then((response) => {
                    console.log(response.data);
                })
                .catch(function (error) {
                    console.log(error);
                });
            
        }  
    }
}
</script>