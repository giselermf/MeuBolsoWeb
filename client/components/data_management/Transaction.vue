<template>
<div id="app" class="ui vertical segments" >
    <div id="app" class="ui horizontal segments" >
      <div class="ui  segment">
          <transaction-search></transaction-search>
      </div>
      <div class="ui  segment">
        <select v-model="grouper">
          <option disabled value="">Please select one</option>
          <option>Type</option>
          <option>Category</option>
          <option>SubCategory</option>
        </select>
       <over-month-with-table :width="500" :height="300" :allData="allData" :show-table="true" :grouper="grouper" ></over-month-with-table>
      </div>
    </div>
    <div class="ui  segment">
      <transaction-table></transaction-table>
    </div> 
    <transaction-edit></transaction-edit>
  </div>
</template>

<script>
import TransactionSearch from "./TransactionSearch.vue";
import TransactionTable from "./TransactionTable.vue";
import OverMonthWithTable from "../data_management/OverMonthBarWithTable";
import TransactionEdit from "./TransactionEdit.vue";

export default {
  components: {
    TransactionSearch,
    TransactionTable,
    OverMonthWithTable,
    TransactionEdit
  },
  data() {
    return {
      appendParams: {},
      allData: null,
      grouper: "Category"
    };
  },
  created() {
    this.getData();
    this.$events.$on("transaction-filter-set", eventData => this.onFilterSet(eventData));
    this.$events.$on("transaction-filter-reset", e => this.onFilterReset());
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
      else return  "?filter=" + JSON.stringify(this.appendParams.filter);
    },
    onFilterSet(filterParams) {
      this.appendParams.filter = filterParams;
      this.getData();
    },
    onFilterReset() {
      delete this.appendParams.filter;
      this.getData();
    }
  }
};
</script>s