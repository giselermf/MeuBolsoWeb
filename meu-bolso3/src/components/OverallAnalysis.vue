<template>
  <div>
    <date-range
      ref="date_range"
      :dateFromDelta="-12"
      :dateToDelta="0"
      @date_range_updated="getData"
    ></date-range>

    <v-layout row wrap>
      <v-flex xs12 sm6 md6>
        <RunningBalanceChart ref="runningBalanceChart" v-bind:allData="allData" :width="800"></RunningBalanceChart>
      </v-flex>

      <v-flex xs12 sm6 md6>
        <v-btn color="primary" v-if="difference>0" class="mx-2" fab>
          <v-icon dark>add</v-icon>
        </v-btn>
        <v-btn color="primary" v-if="difference<=0" lass="mx-2" fab>
          <v-icon dark>remove</v-icon>
        </v-btn>
        {{this.difference}}
      </v-flex>
    </v-layout>

    <v-layout row wrap>
      <v-flex xs12 sm6 md4>
        <v-data-table
          :headers="estateHeaders"
          :items="estateDataBefore"
          class="elevation-1"
          hide-default-footer
          group-by="Type"
        >
          <template v-slot:header.RunningBalance="{ header }">Previous</template>
          <template v-slot:items="props">
            <td class="text-xs-right">{{ props.item.Type }}</td>
            <td class="text-xs-right">{{ props.item.BankName }}</td>
            <td class="text-xs-right">{{ props.item.RunningBalance }}</td>
          </template>

          <template v-slot:header color="primary">
            <td class="text-xs-right font-weight-bold">TOTAL</td>
            <td class="text-xs-right font-weight-bold">{{grandTotalBefore}}</td>
          </template>
        </v-data-table>
      </v-flex>

      <v-flex xs12 sm6 md4>
        <v-data-table
          :headers="estateHeaders"
          :items="estateDataAfter"
          class="elevation-1"
          hide-default-footer
          group-by="Type"
        >
          <template v-slot:header.RunningBalance="{ header }">Current</template>

          <template v-slot:items="props">
            <td class="text-xs-right">{{ props.item.Type }}</td>
            <td class="text-xs-right">{{ props.item.BankName }}</td>
            <td class="text-xs-right">{{ props.item.RunningBalance }}</td>
          </template>

          <template v-slot:header>
            <td class="text-xs-right font-weight-bold">TOTAL</td>
            <td class="text-xs-right font-weight-bold">{{grandTotalAfter}}</td>
          </template>
        </v-data-table>
      </v-flex>
    </v-layout>
  </div>
</template>

<script>
import { HTTP } from "../util/http-common";
import RunningBalanceChart from "../charts/RunningBalanceChart.vue";
import moment from "moment";
import DateRange from "../util/DateRange.vue";

import {
  getGroupByMonthAnd,
  getLabelAndDatabaseBar,
  colors
} from "../util/Utils.js";

export default {
  components: {
    RunningBalanceChart,
    DateRange
  },
  data() {
    return {
      allData: [],
      estateDataBefore: [],
      estateDataAfter: [],
      estateHeaders: [
        { value: "Type", text: "Account Type" },
        { value: "BankName", text: "Bank" },
        { value: "RunningBalance", text: "Current Balance" }
      ],
      grandTotalBefore: 0,
      grandTotalAfter: 0
    };
  },
  mounted() {
    this.getData();
  },
  computed: {
    difference() {
      return (this.grandTotalAfter - this.grandTotalBefore).toFixed(2);
    }
  },
  methods: {
    getParams() {
      let params = {};
      params["bankName"] = this.selectedAccount;
      params["fromDate"] = this.$refs.date_range.getFromDate();
      params["toDate"] = this.$refs.date_range.getToDate();
      return "?filter=" + JSON.stringify(params);
    },
    getData() {
      HTTP.get("transactionsFiltered/" + this.getParams())
        .then(response => {
          this.allData = response["data"]["data"];
        })
        .catch(function(error) {
          console.log(error);
        });
      this.getStateData();
    },
    getStateData() {
      HTTP({
        method: "get",
        url: "estate/?Date=" + this.$refs.date_range.getFromDate()
      })
        .then(response => {
          this.estateDataBefore = response["data"]["data"];
          this.grandTotalBefore = this.estateDataBefore
            .reduce((partial_sum, a) => partial_sum + a.RunningBalance, 0)
            .toFixed(2);
        })
        .catch(function(error) {
          console.log(error);
        });

      HTTP({
        method: "get",
        url: "estate/?Date=" + this.$refs.date_range.getToDate()
      })
        .then(response => {
          this.estateDataAfter = response["data"]["data"];
          this.grandTotalAfter = this.estateDataAfter
            .reduce((partial_sum, a) => partial_sum + a.RunningBalance, 0)
            .toFixed(2);
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    search(filterParams) {
      this.getData();
    }
  }
};
</script>

<style>
table.v-table tbody td,
table.v-table tbody th {
  height: 31px;
}
</style>
