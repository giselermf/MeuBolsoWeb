<template>
    <div >
        <account-select-combo :fromDate="fromDate" :toDate="toDate" :includeAll=false :accountTypes="accountTypes" ref="account_combo" ></account-select-combo>
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
        <category-select-combos ref="search_typecombos" :accountTypes="accountTypes"></category-select-combos>

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
import CategorySelectCombos from "../util/CategorySelectCombos.vue"
import AccountSelectCombo from "../util/AccountSelectCombo.vue"
import DateRange from "../util/DateRange.vue";
import moment from "moment";

export default { 
    
  components: {
    CategorySelectCombos, DateRange, AccountSelectCombo
  },
  data() {
    return {
      Description: null,
      SubCategory: null,
      fromAmount: null,
      toAmount: null,
      fromDate: null,
      toDate: null,
      accountTypes: ['Credit Card', 'Checking Account']
    };
  },
  mounted() {
    this.setDateRangeDefault();
    this.search();
    this.fromDate = moment(this.$refs.cashFlow_range.fromDate).format("YYYY-MM-DD");
    this.toDate = moment(this.$refs.cashFlow_range.toDate).format("YYYY-MM-DD");
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
      this.$refs.account_combo.resetValues();
      this.Description = null;
      this.SubCategory = null;
      this.fromAmount = null;
      this.toAmount = null;
      this.setDateRangeDefault();
      this.$refs.search_typecombos.resetValues();
      this.search();
    },
    search: function() {
        this.fromDate = moment(this.$refs.cashFlow_range.fromDate).format("YYYY-MM-DD");
        this.toDate = moment(this.$refs.cashFlow_range.toDate).format("YYYY-MM-DD");
        let params = {
            category: this.$refs.search_typecombos.getSelectedCategory(),
            subcategory: this.$refs.search_typecombos.getSelectedSubCategory(),
            type: this.$refs.search_typecombos.getSelectedType(),
            bankName: this.$refs.account_combo.getSelectedAccount(),
            fromAmount: this.fromAmount,
            toAmount: this.toAmount,
            fromDate: this.fromDate,
            toDate: this.toDate,
            Description: this.Description,
      };
      this.$events.fire("transaction-filter-set", addFilterParam(params));
    },
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
