<template>
<div  class="column is-one-third">
  <article class="message" style="width: 400px; padding: 20px;">
    <div class="message-header" style = "height: 70px;" >
      <p>{{investment.BankName}}</p>
      <button class="delete" aria-label="delete"></button>
    </div>
    <div class="message-body">
        <div><label>Balance: {{investment.RunningBalance}}</label></div>
        <div><label>Date: {{investment.Date}}</label></div>
      
        <div class="field has-addons" style="padding-top: 8px;" >
          <div class="control">
              <input v-model="amount"  class="input" type="text" placeholder="Balance">
          </div>
          <div class="control" @click="updateRunningBalance">
              <a class="button is-link">
              Update
              </a>
          </div>
          </div>
    </div>
  </article>
</div>
</template>

<script>
import moment from "moment";

export default {
  props: ["investment"],
  components: {},
  data() {
    return {
      category_id: null,
      description: null,
      amount: null
    };
  },
  mounted() {},
  methods: {
    getRunningBalance() {
      if (this.investment.RunningBalance != null) return this.investment.RunningBalance;
      else return 0;
    },
    updateRunningBalance() {
      if (this.amount == null || this.amount == 0) return;
      var axios = require("axios");
      var querystring = require("querystring");
      axios
        .post(
          "http://127.0.0.1:5000/transactions/",
          querystring.stringify({
            Description : "Balance Adjustment",
            TransactionNumber: "...",
            Currency: "EUR",
            Amount: this.amount - this.getRunningBalance(),
            BankName: this.investment.BankName,
            AmountEUR: this.amount - this.getRunningBalance() ,
            RunningBalance: this.amount,
            Date: moment().format("YYYY-MM-DD"),
            Type: "Transfer",
            Category: "Transfer",
            SubCategory: "Transfer"
          })
        )
        .then(response => {
          this.investment.RunningBalance = this.amount;
          this.investment.Date = moment().format("YYYY-MM-DD");
        })
        .catch(function(error) {
          console.log(error);
        });
    }
  }
};
</script>