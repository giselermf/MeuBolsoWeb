<template>
  <div>
    <v-layout row wrap>
      <v-flex xs12 sm6 md6>
        <v-text-field v-model="folder" :counter="100" label="Source of bank files *" required></v-text-field>
      </v-flex>
      <v-flex xs12 sm6 md6>
        <v-btn color="primary" @click="processData">Process Data</v-btn>
      </v-flex>
      <pending-reconciliation
        @reconcilitions-refresh="removeFromData"
        v-for="row in allData"
        :key="row.id"
        :row="row"
        :columns="columns"
      ></pending-reconciliation>
    </v-layout>
    <p></p>
  </div>
</template>

<script>
import PendingReconciliation from "./PendingReconciliation.vue";
import { HTTP } from "../util/http-common";
import querystring from "querystring";

export default {
  components: {
    PendingReconciliation
  },
  data: function() {
    return {
      columns: ["Old Transaction", "New Transaction", "Actions"],
      folder: "/Users/gisele/Documents/bankFiles/",
      allData: null
    };
  },
  mounted() {
    this.search();
  },
  methods: {
    removeFromData(e) {
      this.allData = this.allData.filter(element => element.id != e.data.data);
    },
    search() {
      HTTP.get("PendingReconciliationTransactions/")
        .then(response => {
          this.allData = response["data"]["data"];
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    processData() {
      HTTP.post("processData/", querystring.stringify({ folder: this.folder }))
        .then(response => {
          this.allData = response["data"]["data"];
        })
        .catch(function(error) {
          console.log(error);
        });
    }
  }
};
</script>