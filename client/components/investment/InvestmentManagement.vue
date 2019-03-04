<template>
  <div>
    <div class="ui segment">
      <div class="field is-horizontal-left" >
        <div class="field-body">
          <div class="field is-grouped">
              <account-select-combo :includeAll=false :accountTypes="accountTypes" ref="account_combo" ></account-select-combo>
              <div class="field-label">
                  <label class="label">Running Balance: </label>
              </div>
              <div class="field-body field is-grouped">
                  {{this.getRunningBalance()}}
              </div>
           </div>
        </div>
      </div>
    </div>
    <div class="ui segment">
      <transaction-table :params="appendParams"></transaction-table>
    </div> 
  </div>
</template>
<script>

import {HTTP} from '../util/http-common';
import AccountSelectCombo from "../util/AccountSelectCombo.vue"
import TransactionTable from "../transaction/TransactionTable.vue";
import { addFilterParam } from "../util/Utils.js";


export default {
  components: {AccountSelectCombo , TransactionTable},
  data() {
    return {
      accountTypes: ["Savings"], 
      appendParams: {},
      runningBalanceForAllSavings: null
    };
  },
  mounted() {
    this.$watch(() => this.$refs.account_combo.getSelectedAccount(), (value) => { this.search(); })
    this.getCurrentState();
  },
  methods: {
    getRunningBalance() {
      if (this.runningBalanceForAllSavings != undefined) {
        let selectedBank = this.runningBalanceForAllSavings.filter(x => x.BankName == this.$refs.account_combo.getSelectedAccount())[0]
        if (selectedBank != undefined) 
          return Math.round(selectedBank.RunningBalance, 2);
      }
      return null;
    },
    getCurrentState() {
      HTTP.get("estate/")
      .then(response => {
        this.runningBalanceForAllSavings = response["data"].data;
      })
      .catch(function(error) {
        console.log(error);
      });
    },
    search() {
      this.appendParams.filter = {bankName: this.$refs.account_combo.getSelectedAccount()};
      this.$events.fire("transaction-filter-set", addFilterParam(this.appendParams.filter));
    }
  }
};
</script>