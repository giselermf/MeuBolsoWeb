<template>
  <div id="app" class="ui horizontal segments">
    <investment-card v-for="data in allData" :key="data.BankName" :investment="data"  ></investment-card>
  </div>
</template>

<script>

import InvestmentCard from "./InvestmentCard.vue"
import CallServer from "../util/CallServer.js";

export default {
  mixins: [CallServer],
  components: { InvestmentCard },
  data() {
    return {
      invest: null,
      description: null,
    };
  },
  watch: {
    allData: function(val) {
      this.setData();
    },
  },
  mounted() {
    this.getAllData("Investment", ''); 
  },
  methods: {
    setData: function() {
      console.log('investments', this.allData)
    }
  }
};
</script>