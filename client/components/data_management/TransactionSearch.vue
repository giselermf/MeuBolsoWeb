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
            </div>
            <div>
                <label class="form-label">Amount:</label>
                <input placeholder="from" v-model="fromAmount" class="form-field-small"/> 
                <input placeholder="to" v-model="toAmount" class="form-field-small"/> 
            </div>
            <div>
                <label class="form-label">Description:</label>
                <input placeholder="" v-model="description" class="form-field"/> 
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
      description: null,
      fromAmount: null,
      toAmount: null,
      fromDate: null,
      toDate: null,
    };
  },
  mounted() {
    this.fromDate = moment(new Date())
      .subtract(1, "month")
      .startOf("month")
      .format("YYYY-MM-DD");
    this.toDate = moment(new Date()).subtract(1, "month").endOf("month").format("YYYY-MM-DD");
    this.getCategoriesFromServer();
    this.search();
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
      this.description = null;
      this.fromAmount = null;
      this.toAmount = null;
      this.fromDate = null;
      this.toDate = null;
      this.$events.fire("filter-reset");
    },
    search: function() {
      let params = {
        filterType: "Transactions",
        params: {
            Categories: this.selectedCategories,
            SubCategories: this.selectedSubategories,
            Types: this.selectedTypes,
            bankName: this.selectedBank,
            fromAmount: this.fromAmount,
            toAmount: this.toAmount,
            fromDate: this.fromDate,
            toDate: this.toDate,
            description: this.description,
            Currencies: this.selectedCurrencies
        }
      };
      this.$events.fire("filter-set", addFilterParam('Transactions', params));
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
