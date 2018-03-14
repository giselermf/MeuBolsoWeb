<template>
    <div id="app" class="ui vertical segments" >
        <div class="ui  segment">         
            <div>
                <label class="form-label">Bank:</label>
                <select class="form-field" v-model="selectedBank">
                    <option v-for="bank in getFilterValue('BankName')" v-bind:key="bank.value" v-bind:value="bank.value">
                        {{ bank.value }}
                    </option>
                </select>
            </div> 
            <div>
                <label class="form-label">Date:</label>
                <input placeholder="from" v-model="fromDate" class="form-field-small"/> 
                <input placeholder="to" v-model="toDate" class="form-field-small"/> 
                <select v-model="dateRangeOption" @change="setDateRange()" >
                    <option>Current Month</option>
                    <option>Previous Month</option>
                    <option>Last 3 Months</option>
                    <option>Last 6 Months</option>
                </select>
            </div>
            <div>
                <label class="form-label">Amount:</label>
                <input placeholder="from" v-model="fromAmount" class="form-field-small"/> 
                <input placeholder="to" v-model="toAmount" class="form-field-small"/> 
            </div>
            <div>
                <label class="form-label">Description:</label>
                <input placeholder="" v-model="Description" class="form-field"/> 
            </div>
        </div>
        <div class="ui  segment">
            <div>
                <label class="form-label">Transaction Type:</label>
                <div class="multiple-select" >
                    <ul>
                        <li v-for="transaction_type in getFilterValue('Type')" v-bind:key="transaction_type.value">
                            <input type="checkbox" :id="transaction_type.value" :value="transaction_type.value" v-model="selectedTypes">
                            <label :for="transaction_type.value">{{transaction_type.value}}</label>
                        </li>
                    </ul>
                </div>
            </div>
            <div>
                <label class="form-label">Category:</label>
                <div class="multiple-select" >
                    <ul>
                        <li v-for="category in getFilterValue('Category')" v-bind:key="category.value">
                            <input type="checkbox" :id="category.value" :value="category.value" v-model="selectedCategories">
                            <label :for="category.value">{{category.value}}</label>
                        </li>
                    </ul>
                </div>
            </div> 
            <div>
                <label class="form-label">SubCategory:</label>
                <input placeholder="" v-model="SubCategory" class="form-field"/> 
            </div>
        </div>
        <div id="app" class="ui horizontal segments" >
            <div class="ui  segment" style="display: flex;justify-content: center;padding-top: 1em">
                <button type="button" @click="search()" >Search</button>
                <button type="button" @click="reset()" >Reset</button>
            </div>
        </div>
    </div>
</template>

<script>
import moment from "moment";
import { addFilterParam } from "../charts/ChartUtils.js";

export default {
  data() {
    return {
      selectedCategories: [],
      selectedSubategories: [],
      selectedCurrencies: [],
      selectedTypes: [],
      selectedBank: null,
      all_filter_data: [],
      Description: null,
      SubCategory: null,
      fromAmount: null,
      toAmount: null,
      fromDate: null,
      toDate: null,
      dateRangeOption: "Current Month"
    };
  },
  mounted() {
    this.setDateRange();
    this.getCategoriesFromServer();
  },
  methods: {
    getFilterValue: function(fieldName) {
      var values = this.all_filter_data.map(x => {
        return x[fieldName];
      });
      var unique = values.filter((v, i, a) => a.indexOf(v) === i).sort();
      return unique.map(obj => {
        return { value: obj };
      });
    },
    reset: function() {
      this.selectedCategories = [];
      this.selectedSubategories = [];
      this.selectedCurrencies = [];
      this.selectedTypes = [];
      this.selectedBank = null;
      this.Description = null;
      this.SubCategory = null;
      this.fromAmount = null;
      this.toAmount = null;
      this.fromDate = null;
      this.toDate = null;
      this.dateRangeOption = "Current Month";
      this.$events.fire("transaction-filter-reset");
    },
    search: function() {
      let params = {
        Categories: this.selectedCategories,
        SubCategories: this.selectedSubategories,
        Types: this.selectedTypes,
        bankName: this.selectedBank,
        fromAmount: this.fromAmount,
        toAmount: this.toAmount,
        fromDate: this.fromDate,
        SubCategory: this.SubCategory,
        toDate: this.toDate,
        Description: this.Description,
        Currencies: this.selectedCurrencies
      };
      this.$events.fire("transaction-filter-set", addFilterParam(params));
    },
    setDateRange: function() {
      let begin, end;

      let end_of_last_month = moment(new Date())
        .subtract(1, "month")
        .endOf("month");
      let today = moment(new Date());
      if (this.dateRangeOption == "Current Month") {
        begin = moment(new Date()).startOf("month");
        end = today;
      } else if (this.dateRangeOption == "Previous Month") {
        begin = today.subtract(1, "month").startOf("month");
        end = end_of_last_month;
      } else if (this.dateRangeOption == "Last 3 Months") {
        begin = today.startOf("month").subtract(3, "month");
        end =  moment(new Date())
      } else if (this.dateRangeOption == "Last 6 Months") {
        begin = today.startOf("month").subtract(6, "month");
        end =  moment(new Date());
      }
      this.fromDate = begin.format("YYYY-MM-DD");
      this.toDate = end.format("YYYY-MM-DD");
      this.search();
    },
    getCategoriesFromServer: function() {
      var axios = require("axios");
      var querystring = require("querystring");
      axios
        .get("http://127.0.0.1:5000/getFilterData/")
        .then(response => {
          this.all_filter_data = response["data"];
        })
        .catch(function(error) {
          console.log(error);
        });
    }
  }
};
</script>
