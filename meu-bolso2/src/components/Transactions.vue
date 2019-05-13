<template>
  <div>
    <v-layout row wrap>
      <v-flex xs12 sm6 md6>
        <v-flex>
          <AccountSelectCombo
            ref="account_combo"
            @new-selected-account="refreshAccount"
            :accountTypes="accountTypes"
            :dateFrom="dateFrom"
            :dateTo="dateTo"
          ></AccountSelectCombo>
        </v-flex>
        <v-layout row wrap>
          <v-flex xs12 sm6 md3>
            <v-card-text>Date range</v-card-text>
          </v-flex>
          <v-flex xs12 sm6 md4>
            <v-menu
              :close-on-content-click="false"
              :nudge-right="40"
              lazy
              transition="scale-transition"
              offset-y
              full-width
              min-width="290px"
            >
              <template v-slot:activator="{ on }">
                <v-text-field
                  v-model="dateFrom"
                  label="Date From"
                  prepend-icon="event"
                  readonly
                  v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker v-model="dateFrom" @input="menuDF = false"></v-date-picker>
            </v-menu>
          </v-flex>

          <v-flex xs12 sm6 md4>
            <v-menu
              :close-on-content-click="false"
              :nudge-right="40"
              lazy
              transition="scale-transition"
              offset-y
              full-width
              min-width="290px"
            >
              <template v-slot:activator="{ on }">
                <v-text-field
                  v-model="dateTo"
                  label="Date To"
                  prepend-icon="event"
                  readonly
                  v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker v-model="dateTo" @input="menuDT = false"></v-date-picker>
            </v-menu>
          </v-flex>
        </v-layout>
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
      <v-flex xs12 sm6 md6 >
        <div>
          <v-tabs color="cyan" dark slider-color="yellow">
            <v-tab href="#tab-1">Over Month</v-tab>
            <v-tab href="#tab-2">Running Balance</v-tab>
            <v-tab-item :value="'tab-1'">
              <v-card flat>
                <v-combobox
                  v-model="grouper"
                  :items="['Type', 'Category', 'SubCategory']"
                  label="Please select one"
                ></v-combobox>
                <over-month-with-table
                  :height="200"
                  :allData="allData"
                  :grouper="grouper"
                ></over-month-with-table>
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
    <transactions-table
      @refresh-transaction-table-data="getData"
      v-bind:BankName="selectedAccount"
      :allData="allData"
    ></transactions-table>
  </div>
</template>

<script>
import TransactionsTable from "./TransactionsTable.vue";
import moment from "moment";
import RunningBalanceChart from "./RunningBalanceChart.vue";
import { HTTP } from "../util/http-common";
import AccountSelectCombo from "../util/AccountSelectCombo.vue";
import OverMonthWithTable from "./OverMonthBarWithTable.vue";

export default {
  props: {
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
    OverMonthWithTable
  },
  data: () => ({
    allData: [],
    min: -10000,
    max: 10000,
    slider: 40,
    range: [-10000, 10000],
    selectedAccount: null,
    grouper: "Category",
    dateFrom: null,
    dateTo: null
  }),
  mounted() {
    this.dateFrom = moment(new Date())
      .add(this.dateFromDelta, "month")
      .startOf("month")
      .format("YYYY-MM-DD");
    this.dateTo = moment(new Date())
      .add(this.dateToDelta, "month")
      .endOf("month")
      .format("YYYY-MM-DD");
    this.getData();
  },
  watch: {
    dateFrom: function(newVal, oldVal) {
      this.getData();
    },
    dateTo: function(newVal, oldVal) {
      this.getData();
    },
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
      params["fromDate"] = this.dateFrom;
      params["toDate"] = this.dateTo;
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
