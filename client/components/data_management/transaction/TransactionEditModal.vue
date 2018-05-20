

<template>
   <transition name="modal">
  <div class="modal modal-mask ">
  <div class="modal-background"></div>
  <div class="modal-card">
    <header class="modal-card-head">
      <p class="modal-card-title">Edit Transaction</p>
    </header>
    <section class="modal-card-body">
        <div class="field is-horizontal" >
            <div class="field-label">
              <label class="label">Bank</label>
            </div>
            <div class="field-body">
              <div class="field is-grouped">
                <p class="control is-expanded">
                  {{ selectedTransaction.BankName }}
                </p>
              </div>
            </div>
        </div>
        <div class="field is-horizontal" >
            <div class="field-label">
              <label class="label">Description</label>
            </div>
            <div class="field-body">
              <div class="field is-grouped">
                <p class="control is-expanded">
                  {{ selectedTransaction.Description }}
                </p>
              </div>
            </div>
        </div>
        <div v-if="split" class="field is-horizontal" >
            <div class="field-label">
              <label class="label">Amount</label>
            </div>
            <div class="field-body">
              <div class="field is-grouped">
                <p class="control is-expanded">
                  <input class=" field control input" placeholder="value" v-model="newAmount"/>
                </p>
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
import CategorySelectCombos from "../../util/CategorySelectCombos.vue";

export default {
  props : ["split", "selectedTransaction"],
  components: {
    CategorySelectCombos
  },
  data() {
    return {
      newAmount: this.selectedTransaction.AmountEUR
    }
  },
  mounted() {
    this.$refs.typecombos.selectedType = this.selectedTransaction.Type;
    this.$refs.typecombos.selectedCategory = this.selectedTransaction.Category;
    this.$refs.typecombos.selectedSubCategory = this.selectedTransaction.SubCategory;
  },
  methods: {
    onSplit(eventData) {
      console.log('onSplit', this.selectedTransaction);
    },
    saveTransaction() {
      console.log('saving');
      var axios = require("axios");
      var querystring = require("querystring");
      axios
        .post(
          "http://127.0.0.1:5000/transactions/",
          querystring.stringify({
            transaction_id: this.selectedTransaction.id,
            category_id: this.$refs.typecombos.getSelectedCategoryId()
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
      console.log('spliting');
      var axios = require("axios");
      var querystring = require("querystring");
      axios
        .post(
          "http://127.0.0.1:5000/splitTransaction/",
          querystring.stringify({
            transaction_id: this.selectedTransaction.id,
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
    CloseModal() {
      this.$events.fire("close-transaction-split-modal");
    },
    SaveAndCloseModal() {
      if (this.split) this.splitTransaction();
      else this.saveTransaction();
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
