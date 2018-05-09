<template>
    <div >
        <div class="field is-horizontal" >
            <div class="field-label">
                <label class="label">Bank</label>
            </div>
            <div class="field-body">
                <div class="field is-grouped">
                    <p class="control is-expanded">
                        <select class="select" v-model="selectedBank" @change="search()">
                            <option v-for="bank in getFilterValue('BankName')" v-bind:key="bank.value" v-bind:value="bank.value">
                                {{ bank.value }}
                            </option>
                        </select> 
                    </p>
                </div>
            </div>
        </div>

        <div class="field is-horizontal" >
            <div class="field-label">
                <label class="label">Date</label>
            </div>
            <div class="field-body">
                <div class="field is-grouped">
                    <p class="control is-expanded">
                            <datepicker v-model="fromDate" placeholder="from" :minimumView="'day'" :maximumView="'day'"></datepicker>
                    </p>
                    <p class="control is-expanded">
                        <datepicker v-model="toDate" placeholder="to" :minimumView="'day'" :maximumView="'day'"></datepicker>
                    </p>
            </div></div>
        </div>

        <div class="field is-horizontal" >
            <div class="field-label">
                <label class="label">Amount</label>
            </div>
            <div class="field-body">
                <div class="field is-grouped">
                    <p class="control is-expanded">
                        <input class=" field control input"  placeholder="from" v-model="fromAmount"/>
                    </p>
                    <p class="control is-expanded">
                        <input  class=" field control input" placeholder="to" v-model="toAmount"/>
                    </p>
            </div></div>
        </div>


        <div class="field is-horizontal" >
            <div class="field-label">
                <label class="label">Description</label>
            </div>
            <div class="field-body">
                <div class="field is-grouped">
                    <p class="control is-expanded">
                        <input class="control input"  placeholder="" v-model="Description"/> 
                    </p>
            </div></div>
        </div>

        <div class="field is-horizontal" >
            <div class="field-label">
                <label class="label">Type and Category</label>
            </div>
            <div class="field-body">
                <div class="field is-grouped">
                    <p class="control is-expanded">
                        <div class="select is-multiple select-enhancement" >
                            <select class="select" multiple size="6" v-model="selectedTypes">
                                <option v-for="transaction_type in getFilterValue('type')" v-bind:key="transaction_type.value">{{transaction_type.value}}</option>
                            </select>
                        </div>
                    </p>
                    <p class="control is-expanded">
                        <div class="select is-multiple select-enhancement">
                            <select class="select" multiple size="15" v-model="selectedCategories" >
                                <option v-for="category in getFilterValue('category')" v-bind:key="category.value">{{category.value}}</option>
                            </select>
                        </div>
                    </p>
                </div>
            </div>
        </div>

        <div class="field is-horizontal" >
            <div class="field-label">
                <label class="label">SubCategory</label>
            </div>
            <div class="field-body">
                <div class="field is-grouped">
                    <p class="control is-expanded">
                        <input class="control input" placeholder="" v-model="SubCategory"/> 
                    </p>
                </div>
            </div>
        </div>

        <div class="field is-grouped is-grouped-centered">
            <p class="control">
                <button class="button is-link"  @click="search()" >Search</button>
            </p>
            <p class="control">
                <button class="button is-link" @click="reset()" >Reset</button>
            </p>
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
    this.setDateRangeDefault();
  },
  mounted() {
    this.search();
  },
  methods: {
    setDateRangeDefault() {
      this.fromDate = moment(new Date())
        .startOf("month")
        .subtract(2, "month")
        .format("YYYY-MM-DD");
      this.toDate = moment(new Date())
        .add(2, "month")
        .format("YYYY-MM-DD");
    },
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
      this.setDateRangeDefault();
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

<style>
input,
select {
    width: 100%;
    height: 2.25em;
    padding-bottom: calc(0.375em - 1px);
    padding-left: calc(0.625em - 1px);
    padding-right: calc(0.625em - 1px);
    padding-top: calc(0.375em - 1px);
}
</style>
