<template>
  <div id="app" class="ui vertical segments">
    <div id="app" class="ui horizontal segments">
      <div class="ui segment four wide column">
        <transaction-search></transaction-search>
      </div>
      <div class="ui segment eight wide column">
        <div class="tabs help-tabs">
          <ul>
            <li :class="[ tab_value === 'table' ? 'is-active' : '']">
              <a @click="tab_value='table'">Transaction Table</a>
            </li>
            <li :class="[ tab_value === 'flow' ? 'is-active' : '']">
              <a @click="tab_value='flow'">Cash Flow</a>
            </li>
          </ul>
        </div>

        <div class="box help-content">
          <code v-if="tab_value ==='table'">
            <select v-model="grouper">
              <option disabled value>Please select one</option>
              <option>Type</option>
              <option>Category</option>
              <option>SubCategory</option>
            </select>
            <over-month-with-table
              :height="300"
              :allData="allData"
              :show-table="true"
              :grouper="grouper"
            ></over-month-with-table>
          </code>
          <code v-if="tab_value ==='flow'">
            <RunningBalanceChart ref="runningBalanceChart" :allData="allData"></RunningBalanceChart>
          </code>
        </div>
      </div>
    </div>

    <div class="ui segment">
      <transaction-table :params="appendParams"></transaction-table>
    </div>
  </div>
</template>

<script>
import TransactionSearch from "./TransactionSearch.vue";
import TransactionTable from "./TransactionTable.vue";
import OverMonthWithTable from "./OverMonthBarWithTable.vue";
import { HTTP } from "../util/http-common";
import moment from "moment";
import { colors } from "../util/Utils.js";
import RunningBalanceChart from "./RunningBalanceChart.vue";

export default {
  components: {
    TransactionSearch,
    TransactionTable,
    OverMonthWithTable,
    RunningBalanceChart
  },
  data() {
    return {
      appendParams: {},
      allData: null,
      grouper: "Category",
      tab_value: "table",
      chartData: {}
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
      if (this.getFilterParam() != "") {
        //don't call without filter
        HTTP({
          method: "get",
          url: "transactionsFiltered/" + this.getFilterParam()
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
    }
  }
};
</script>