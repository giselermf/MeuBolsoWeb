<template>
  <div id="app" class="columns is-multiline">
    <investment-card v-for="data in allData" :key="data.BankName" :investment="data"  ></investment-card>
  </div>
</template>

<script>

import InvestmentCard from "./InvestmentCard.vue"
import {HTTP} from '../util/http-common';

export default {
  components: { InvestmentCard },
  data() {
    return {
      allData: null
    };
  },
  mounted() {
    HTTP
      .get("Investment/")
      .then(response => {
        this.allData = response["data"]["data"];
      })
      .catch(function(error) {
        console.log(error);
      });
  },

};
</script>