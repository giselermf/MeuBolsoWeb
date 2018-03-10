<template>
<div id="app" class="ui vertical segments" >
    <div id="app" class="ui horizontal segments" >
      <div class="ui  segment">
          <transaction-search></transaction-search>
      </div>
      <div class="ui  segment">
       <over-month-with-table :width="500" :height="300" :allData="allData" :show-table="false" ></over-month-with-table>
      </div>
    </div>
    <div class="ui  segment">
      <transaction-table></transaction-table>
    </div> 
  </div>
</template>

<script>
import TransactionSearch from "./TransactionSearch.vue";
import TransactionTable from "./TransactionTable.vue";
import OverMonthWithTable from "../data_management/OverMonthBarWithTable";

export default {
  components: {
    TransactionSearch,
    TransactionTable,
    OverMonthWithTable
  },
  data() {
    return {
      appendParams: {},
      allData: null
    };
  },
  mounted() {
    this.$events.$on("filter-set", eventData => this.onFilterSet(eventData));
    this.$events.$on("filter-reset", e => this.onFilterReset());
    this.getData();
  },
  methods: {
    getData() {
      let axios = require("axios");
      let querystring = require("querystring");
      axios
        .get("http://127.0.0.1:5000/transactionsFiltered/" + this.getFilterParam())
        .then(response => {
          this.allData = response["data"]["data"];
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    getFilterParam() {
      if ( this.appendParams.filter == undefined ) return "";
      else return this.appendParams.filter;
    },
    onFilterSet(filterParams) {
      this.appendParams.filter = filterParams;
    },
    onFilterReset() {
      delete this.appendParams.filter;
    }
  }
};
</script>s