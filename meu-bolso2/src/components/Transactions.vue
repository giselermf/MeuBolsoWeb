<template>
  <div>
    <v-container fluid>
      <v-layout row wrap>
        <v-flex xs12 sm6 md6>
          <v-flex>
            <AccountSelectCombo
              ref="account_combo"
              @new-selected-account="refreshAccount"
              :accountTypes="accountTypes"
            ></AccountSelectCombo>
          </v-flex>
          <date-range
            ref="date_range"
            :dateFromDelta="dateFromDelta"
            :dateToDelta="dateToDelta"
            @date_range_updated="getData"
          ></date-range>
          <v-layout row wrap>
            <v-flex xs12 sm6 md3>
              <v-card-text>Amount range (EUR)</v-card-text>
            </v-flex>
            <v-flex xs12 sm6 md8>
              <v-card-text>
                <v-layout row>
                  <v-flex shrink style="width: 100px">
                    <v-text-field
                      v-model="range[0]"
                      class="mt-0"
                      hide-details
                      single-line
                      type="number"
                    ></v-text-field>
                  </v-flex>
                  <v-flex class="px-3">
                    <v-range-slider v-model="range" :max="max" :min="min"></v-range-slider>
                  </v-flex>
                  <v-flex shrink style="width: 100px">
                    <v-text-field
                      v-model="range[1]"
                      class="mt-0"
                      hide-details
                      single-line
                      type="number"
                    ></v-text-field>
                  </v-flex>
                </v-layout>
              </v-card-text>
            </v-flex>
          </v-layout>
        </v-flex>
        <v-flex xs12 sm6 md6>
          <div>
            <v-tabs color="grey" dark slider-color="yellow">
              <v-tab v-if="showOverMonth" href="#tab-1">Over Month</v-tab>
              <v-tab href="#tab-2">Running Balance</v-tab>
              <v-tab-item v-if="showOverMonth" :value="'tab-1'">
                <v-card flat>
                  <over-month-with-table :height="200" :allData="allData"></over-month-with-table>
                </v-card>
              </v-tab-item>
              <v-tab-item :value="'tab-2'">
                <v-card flat>
                  <RunningBalanceChart ref="runningBalanceChart" :allData="allData"></RunningBalanceChart>
                </v-card>
              </v-tab-item>
            </v-tabs>
          </div>
        </v-flex>
      </v-layout>
    </v-container>
    <v-container fluid>
      <transactions-table
        @refresh-transaction-table-data="getData"
        v-bind:BankName="selectedAccount"
        :allData="allData"
      ></transactions-table>
    </v-container>
  </div>
</template>

<script>
import TransactionsTable from "./TransactionsTable.vue";
import moment from "moment";
import RunningBalanceChart from "../charts/RunningBalanceChart.vue";
import { HTTP } from "../util/http-common";
import AccountSelectCombo from "../util/AccountSelectCombo.vue";
import OverMonthWithTable from "../charts/OverMonthBarWithTable.vue";
import DateRange from "../util/DateRange.vue";

export default {
  props: {
    showOverMonth: false,
    accountTypes: Array,
    dateFromDelta: {
      type: Number,
      default: -1
    },
    dateToDelta: {
      type: Number,
      default: 1
    }
  },
  name: "Transactions",
  components: {
    TransactionsTable,
    RunningBalanceChart,
    AccountSelectCombo,
    OverMonthWithTable,
    DateRange
  },
  data: () => ({
    allData: [],
    min: -10000,
    max: 10000,
    slider: 40,
    range: [-10000, 10000],
    selectedAccount: null,
  }),
  watch: {
    range: function(newVal, oldVal) {
      this.getData();
    }
  },
  methods: {
    refreshAccount() {
      this.selectedAccount = this.$refs.account_combo.getSelectedAccount();
      this.getData();
    },
    getFilterParams() {
      let params = {};
      params["bankName"] = this.selectedAccount;
      params["fromDate"] = this.$refs.date_range.getFromDate();
      params["toDate"] = this.$refs.date_range.getToDate();
      params["fromAmount"] = this.range[0];
      params["toAmount"] = this.range[1];
      return params;
    },
    getData() {
      HTTP({
        method: "get",
        url:
          "transactionsFiltered/?sort=BankName|asc&filter=" +
          JSON.stringify(this.getFilterParams())
      })
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
