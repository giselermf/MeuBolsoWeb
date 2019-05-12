<template>
  <v-container fluid>
    <v-layout wrap>
      <v-flex xs12>
        <v-combobox
          :multiple="multiple"
          v-model="selectedAccount"
          :items="allActiveAccounts"
          label="Select account"
        ></v-combobox>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import moment from "moment";
import { HTTP } from "./http-common";

export default {
  props: {
    dateFrom: String,
    dateTo: String,
    accountTypes: null,
    multiple: false
  },
  data() {
    return {
      selectedAccount: null,
      allActiveAccounts: []
    };
  },
  created() {
    this.getFilterData();
  },
  watch: {
    selectedAccount: {
      handler(newData, oldData) {
        this.$emit("new-selected-account");
      }
    },
    dateFrom: {
      handler(newData, oldData) {
        this.getFilterData();
      }
    },
    dateTo: {
      handler(newData, oldData) {
        this.getFilterData();
      }
    }
  },
  methods: {
    // selectFirstAccount() {
    //   this.selectedAccount = this.allActiveAccounts[0];
    // },
    setSelectedAccount(BankName) {
      this.selectedAccount = BankName;
    },
    getSelectedAccount() {
      return this.selectedAccount;
    },
    getParams() {
      let params = {};
      if (this.accountTypes) params["type"] = this.accountTypes;
      if (this.accountTypes) params["active"] = true;
      if (this.dateFrom)
        params["dateFrom"] = moment(this.dateFrom).format("YYYY-MM-DD");
      if (this.dateTo)
        params["dateTo"] = moment(this.dateTo).format("YYYY-MM-DD");
      return "?filter=" + JSON.stringify(params);
    },
    getFilterData() {
      HTTP.get("getAllAccounts/" + this.getParams())
        .then(response => {
          this.allActiveAccounts = Object.values(
            response["data"].data.map(e => e.BankName)
          );
        })
        .catch(function(error) {
          console.log(error);
        });
    }
  }
};
</script>

