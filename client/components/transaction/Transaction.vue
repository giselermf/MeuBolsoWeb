<template>
<div id="app" class="ui vertical segments" >
    <div id="app" class="ui horizontal segments" >
      <div class="ui  segment four wide column">
          <transaction-search></transaction-search>
      </div>
      <div class="ui  segment eight wide column">
        <select v-model="grouper">
          <option disabled value="">Please select one</option>
          <option>Type</option>
          <option>Category</option>
          <option>SubCategory</option>
        </select>
       <over-month-with-table :height="300" :allData="allData" :show-table="true" :grouper="grouper" ></over-month-with-table>
      </div>
    </div>
    <div class="ui  segment">
      <transaction-table :params="appendParams" ></transaction-table>
    </div> 
  </div>
</template>

<script>
import TransactionSearch from "./TransactionSearch.vue";
import TransactionTable from "./TransactionTable.vue";
import OverMonthWithTable from "./OverMonthBarWithTable.vue";

export default {
  components: {
    TransactionSearch,
    TransactionTable,
    OverMonthWithTable
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
    this.$events.$on("transaction-filter-set", eventData =>
      this.onFilterSet(eventData)
    );
  },
  methods: {
    getData() {
      let axios = require("axios");
      let querystring = require("querystring");
      if (this.getFilterParam() != "") { //don't call without filter
          axios({
            method:'get',
            url:"http://127.0.0.1:5000/transactionsFiltered/"  + this.getFilterParam()
            })
            .then(response => {
              this.allData = response["data"]["data"];
            })
            .catch(function(error) {
              console.log(error);
            });
        }
    },
    getFilterParam() {
      if (this.appendParams.filter == undefined) return "";
      else return "?filter=" + JSON.stringify(this.appendParams.filter);
    },
    onFilterSet(filterParams) {
      this.appendParams.filter = filterParams;
      this.getData();
    },
  }
};
</script>