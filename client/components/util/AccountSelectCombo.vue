<template>
  <div class="field is-horizontal" >
      <div class="field-label">
          <label class="label">Bank</label>
      </div>
      <div class="field-body field is-grouped">
          <select class="select" v-model="selectedAccount">
              <option v-for="bank in allActiveAccounts" v-bind:key="bank.BankName" v-bind:value="bank">
                  {{ bank.BankName }}
              </option>
          </select> 
      </div>
  </div>  
</template>

<script>
import moment from "moment";

export default {
 // props: ["fromDate", "toDate", "includeAll"],
  props: {
      fromDate: String,
      toDate: String,
      includeAll: {
        type: Boolean,
        default: false
      },
  },
  data() {
    return {
      selectedAccount: {},
      allActiveAccounts: [],
    };
  },
  mounted() {
    this.getFilterData();
  },
  watch: {
    fromDate: {
      handler(newData, oldData) {
        this.getFilterData();
      }
    },
    toDate: {
      handler(newData, oldData) {
        this.getFilterData();
      }
    }
  },
  methods: {
    resetValues() {
      if (this.includeAll) {
        this.selectedAccount = {BankName : "All"}
      } else {
        this.selectedAccount = {};
      }
    },
    getSelectedAccount() {
      if (this.selectedAccount)
        return this.selectedAccount.BankName;
    },
    getCurrency() {
      if (this.selectedAccount)
        return this.selectedAccount.Currency;
    },
    getParams() {
      let params = {};
      if (this.fromDate) params["fromDate"] = moment(this.fromDate).format("YYYY-MM-DD");
      if (this.toDate) params["toDate"] = moment(this.toDate).format("YYYY-MM-DD");
      return "?filter=" + JSON.stringify(params);
    },
    getFilterData() {
      var axios = require("axios");
      var querystring = require("querystring");
      axios
      .get("http://127.0.0.1:5000/getAllAccounts" + this.getParams())
      .then(response => {
          if (this.includeAll) {
            this.selectedAccount = {BankName : "All"},
            this.allActiveAccounts = [{BankName: "All"}];
          } else {
            this.allActiveAccounts = [];
          }
          Array.prototype.push.apply(this.allActiveAccounts, response["data"].data);
      })
      .catch(function(error) {
        console.log(error);
      });
    }
  }
};
</script>