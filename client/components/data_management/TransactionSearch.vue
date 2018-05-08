<template>
    <div id="app" class="ui vertical segments" >
        <div class="ui  segment">         
            <div>
                <label class="form-label">Bank:</label>
                <select class="form-field" v-model="selectedBank" @change="search()">
                    <option v-for="bank in getFilterValue('BankName')" v-bind:key="bank.value" v-bind:value="bank.value">
                        {{ bank.value }}
                    </option>
                </select>
            </div> 
            <div>
                <label class="form-label">Date:</label>
                <datepicker class="date-picker" v-model="fromDate" placeholder="from" :minimumView="'day'" :maximumView="'day'"></datepicker>
                <datepicker class="date-picker" v-model="toDate" placeholder="to" :minimumView="'day'" :maximumView="'day'"></datepicker>
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
                        <li v-for="transaction_type in getFilterValue('type')" v-bind:key="transaction_type.value">
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
                        <li v-for="category in getFilterValue('category')" v-bind:key="category.value">
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
import { addFilterParam } from "../util/Utils.js";
import Datepicker from "vuejs-datepicker";

export default {
  components: {
    Datepicker
  },
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
  created() {
    this.getCategoriesFromServer();
    this.fromDate = moment(new Date())
      .startOf("month")
      .subtract(2, "month")
      .format("YYYY-MM-DD");
    this.toDate = moment(new Date())
      .add(2, "month")
      .format("YYYY-MM-DD");
  },
  mounted() {
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
        SubCategory: this.SubCategory,
        fromDate: this.fromDate, 
        toDate: this.toDate, 
        Description: this.Description,
        Currencies: this.selectedCurrencies
      };
      this.$events.fire("transaction-filter-set", addFilterParam(params));
    },
    getCategoriesFromServer: function() {
      var axios = require("axios");
      var querystring = require("querystring");
      axios
        .get("http://127.0.0.1:5000/getFilterTransactionData/")
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
