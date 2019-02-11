<template>
   <transition name="modal">
  <div class="modal modal-mask ">
  <div class="modal-background"></div>
  <div class="modal-card">
    <header class="modal-card-head">
      <p class="modal-card-title">{{action}} transaction</p>
    </header>
    <section class="modal-card-body">
      <div class="field " >
          <div v-if="action != 'add'" class="field is-horizontal">
              <div class="field-label">
                <label class="label">Bank</label>
              </div>
              <div class="field is-grouped field-body">
                {{ transaction.account }}
              </div>
          </div>
          <div  v-else>
              <account-select-combo ref="account_combo" ></account-select-combo>
          </div>
        </div>
        <div class="field is-horizontal" >
              <div class="field-label">
                <label class="label">Description</label>
              </div>  
              <div class="field is-grouped field-body">
                <div  v-if="action != 'add'" class="field-body">
                    {{ transaction.Description }}
                </div>
                <div  v-else class="field-body">
                  <input class=" field control input" placeholder="value" v-model="transaction.Description "/>
                </div>
                <div class="field-label">
                  <label class="label" style="margin-left: 20px;" >Amount</label>
                </div>
                <div class="field-body">
                  <div class="field is-grouped" v-if="action != 'edit'">
                    <input class="field control input" type="decimal" placeholder="value" v-model="newAmount"/>
                  </div>
                  <div v-else>
                    {{ transaction.Amount }}
                  </div>
                </div>
              </div>
        </div>
        <div v-if="action == 'add'" class="field is-horizontal" >
            <div class="field-label">
              <label class="label">Frequency</label>
            </div>
            <div class="field-body">
              <div class="field is-grouped">
                <input class=" field control input" style="width: 100px;" type="number" value="1" v-model="numberOccurrencies"/>
                <select class="select" v-model="frequency">
                      <option v-for="frequency in getFrequency()" v-bind:key="frequency" v-bind:value="frequency">
                          {{ frequency }}
                      </option>
                  </select>
              </div>
            </div>
        </div>
        <div v-if="action == 'add'" class="field is-horizontal" >
            <div class="field-label">
              <label class="label">Starting at</label>
            </div>
            <div class="field-body">
              <div class="field is-grouped">
                  <datepicker :typeable="true" v-model="fromDate" placeholder="from"></datepicker>

              </div>
            </div>
        </div>

        <category-select-combos ref="typecombos" ></category-select-combos>
        
    </section>
    <footer class="modal-card-foot">
      <button class="button is-success" @click="SaveAndCloseModal">Save</button>
      <button class="button is-success" @click="CloseModal">Close</button>
    </footer>
  </div>
</div>
</transition>
</template>

<script>
import CategorySelectCombos from "../util/CategorySelectCombos.vue";
import AccountSelectCombo from "../util/AccountSelectCombo.vue"
import Datepicker from "vuejs-datepicker";
import moment from "moment";

export default {
  props : ["action", "transaction"],
  components: {
    CategorySelectCombos, AccountSelectCombo, Datepicker
  },
  data() {
    return {
      newAmount: this.transaction.AmountEUR,
      frequency: "Monthly",
      numberOccurrencies: 1,
      fromDate: moment(new Date()).format("YYYY-MM-DD")
    }
  },
  mounted() {
    this.$refs.typecombos.selectedType = this.transaction.Type;
    this.$refs.typecombos.selectedCategory = this.transaction.Category;
    this.$refs.typecombos.selectedSubCategory = this.transaction.SubCategory;
  },
  methods: {
    saveTransfer() {
      var axios = require("axios");
      var querystring = require("querystring");
      axios
        .post(
          "http://127.0.0.1:5000/transfer/",
          querystring.stringify({
            transaction_id: this.transaction.id,
            AmountEUR: this.transaction.AmountEUR,
            Amount: this.transaction.Amount,
            Currency: this.transaction.Currency,
            Date: this.transaction.Date,
            TransactionNumber: this.transaction.TransactionNumber,
            toSelectedBank: this.$refs.typecombos.getSelectedTransferAccount(),
            oldTransferId: this.transaction.TransferId
          })
        )
        .then(response => {
          this.$events.fire("close-transaction-split-modal");
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    saveTransaction() {
      var axios = require("axios");
      var querystring = require("querystring");
      axios
        .post(
          "http://127.0.0.1:5000/transactions/",
          querystring.stringify({
            transaction_id: this.transaction.id,
            category_id: this.$refs.typecombos.getSelectedCategoryId(),
          })
        )
        .then(response => {
          this.$events.fire("close-transaction-split-modal");
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    splitTransaction() {
      var axios = require("axios");
      var querystring = require("querystring");
      axios
        .post(
          "http://127.0.0.1:5000/splitTransaction/",
          querystring.stringify({
            transaction_id: this.transaction.id,
            new_amount_EUR: this.newAmount,
            new_category_id: this.$refs.typecombos.getSelectedCategoryId()
          })
        )
        .then(response => {
          this.$events.fire("close-transaction-split-modal");
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    getFrequency() {
      return ["Weekly", "Monthly", "Quartely", "Yearly"];
    },
    addTransaction() {
      var axios = require("axios");
      var querystring = require("querystring");
      axios
        .post(
          "http://127.0.0.1:5000/addFutureTransactions/",
          querystring.stringify({
            Account: this.$refs.account_combo.getSelectedAccount(),
            Currency: this.$refs.account_combo.getCurrency(),
            AmountEUR: this.newAmount,
            numberOccurrencies: this.numberOccurrencies, 
            frequency: this.frequency,
            fromDate: moment(this.fromDate).format("YYYY-MM-DD"),
            description: this.transaction.Description,
            category_id: this.$refs.typecombos.getSelectedCategoryId(),
          })
        )
        .then(response => {
          this.$events.fire("close-transaction-split-modal");
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    CloseModal() {
      this.$events.fire("close-transaction-split-modal");
    },
    SaveAndCloseModal() {
      if (this.action == 'split') { 
        this.splitTransaction();
      } else if (this.action == 'edit') {
          if (this.$refs.typecombos.selctedSubCategory == 'Transfer') {
            this.saveTransfer();
          } 
          else this.saveTransaction();
      } else if (this.action == 'add') {
          this.addTransaction();
      }
    }
  }
};
</script>

<style>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: table;
  transition: opacity 0.3s ease;
}

.modal-container {
  width: 500px;
  height: 220px;
  margin: 0px auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;
  font-family: Helvetica, Arial, sans-serif;
}

.modal-default-button {
  float: right;
}
</style>
