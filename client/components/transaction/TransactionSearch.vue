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
                    <date-range ref="cashFlow_range" minimumView="day"></date-range>  
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
        <category-select-combos ref="search_typecombos" ></category-select-combos>

        <div class="field is-grouped is-grouped-centered" style="padding-top: 10px;">
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
import { addFilterParam } from "../util/Utils.js";
import Datepicker from "vuejs-datepicker";
import CategorySelectCombos from "../util/CategorySelectCombos.vue"
import DateRange from "../util/DateRange.vue";
import moment from "moment";

export default { 
    
  components: {
    Datepicker, CategorySelectCombos, DateRange
  },
  data() {
    return {
      selectedBank: null,
      all_filter_data: [],
      Description: null,
      SubCategory: null,
      fromAmount: null,
      toAmount: null,
    };
  },
  mounted() {
    this.getCategoriesFromServer();
    this.setDateRangeDefault();
    this.search();
  },
  methods: {
    setDateRangeDefault() {
        this.$refs.cashFlow_range.setRange(-2, 2);
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
      this.selectedBank = null;
      this.Description = null;
      this.SubCategory = null;
      this.fromAmount = null;
      this.toAmount = null;
      this.setDateRangeDefault();
      this.$refs.search_typecombos.resetValues();
      this.search();
    },
    search: function() {
      let params = {
        Category: this.$refs.search_typecombos.getSelectedCategory(),
        SubCategory: this.$refs.search_typecombos.getSelectedSubCategory(),
        Type: this.$refs.search_typecombos.getSelectedType(),
        bankName: this.selectedBank,
        fromAmount: this.fromAmount,
        toAmount: this.toAmount,
        fromDate: moment(this.$refs.cashFlow_range.fromDate).format("YYYY-MM-DD"),
        toDate: moment(this.$refs.cashFlow_range.toDate).format("YYYY-MM-DD"),
        Description: this.Description,
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
