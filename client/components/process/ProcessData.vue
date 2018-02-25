<template>
    <div>
      <button v-on:click="processData">Process Data</button>
        <div>
            <input v-model="folder" placeholder="source of bank files" class="form-field"> <br> 
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