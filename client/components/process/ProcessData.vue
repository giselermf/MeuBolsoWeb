<template>
    <div>
      <div class="field is-horizontal-left" >
          <div class="field-body">
              <div class="field is-grouped">
                  <p class="control is-expanded">
                          <input type="text" class="input" v-model="folder" placeholder="source of bank files"> <br> 
                  </p>
                  <p class="control">
                      <button class="button is-link" v-on:click="processData">Process Data</button>
                  </p>
          </div></div>
      </div>
      <div id="app" class="ui vertical segments" style="overflow-x: auto;">
        <div class="ui vertical segment"  >
            <table  class="vuetable ui blue selectable celled stackable attached table">
            <thead>
                <tr>
                    <th v-for="col in columns" :key="col" >{{col}}</th>
                </tr>
            </thead>
                <tbody>
                    <pending-reconciliation
                            v-for="row in allData" :key="row.id"
                            :row="row"
                            :columns="columns" 
                    ></pending-reconciliation>
                </tbody>
            </table>
        </div>
    </div>
    </div>
</template>

<script>
import PendingReconciliation from "./PendingReconciliation.vue";
import {HTTP} from '../util/http-common';
import querystring  from "querystring"

export default {
  components: {
    PendingReconciliation
  },
  data: function () {
        return {
            columns: ["Old Transaction", "New Transaction", "Actions"],
            folder: "/Users/gisele/Documents/bankFiles/",
            allData: null
        }
    },
    mounted() {
        this.search();
        this.$events.$on("reconcilitions-refresh", e => this.removeFromData(e));
    },
    methods: {
        removeFromData(e) {
            this.allData = this.allData.filter(
                element =>
                    element.id != e.data.data
                );
        },
        search() {
            HTTP
            .get("PendingReconciliationTransactions/")
            .then(response => {
                this.allData = response["data"]["data"];
            })
            .catch(function(error) {
                console.log(error);
            });
        },
        processData() {
            HTTP.post(
                "processData/",
                querystring.stringify({folder: this.folder}))
                .then(response => {
                    this.allData = response["data"]["data"];
                })
                .catch(function(error) {
                    console.log(error);
                });
            
        }  
    }
}
</script>