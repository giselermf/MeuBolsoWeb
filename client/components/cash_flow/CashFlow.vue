<template>
  <div id="app" class="ui vertical segments" >
    <div id="app" class="ui horizontal segments" >
      <div class="ui  segment four column">
        <account-select-combo :fromDate="fromDate" :toDate="toDate" :includeAll=true ref="account_combo_all" ></account-select-combo>
        <div class="field is-horizontal" >
            <div class="field-label">
                <label class="label">Date</label>
            </div>
            <div class="field-body">
                <div class="field is-grouped">
                    <date-range ref="cashFlow_range" minimumView="month"></date-range>  
                </div>
            </div>
        </div>
        <div class="field is-grouped is-grouped-centered" style="padding-top: 10px;">
            <p class="control">
                <button class="button is-link"  @click="search()" >Search</button>
            </p>
        </div>
      </div>
      <div class="ui  segment eight wide column">
          <meu-bolso-line :height="height" :chartData="chartData" :title="title" xLabel="Date" datasetLabel="BankName"></meu-bolso-line>
      </div>
    </div>
    <div class="ui  segment">
      <transaction-table :params="appendParams"></transaction-table>
    </div> 
  </div>
</template>

<script>
import DateRange from "../util/DateRange.vue";
import moment from "moment";
import TransactionTable from "../transaction/TransactionTable.vue";
import meuBolsoLine from "../charts/meuBolsoLine.js";
import { colors } from "../util/Utils.js";
import AccountSelectCombo from "../util/AccountSelectCombo.vue"
import {HTTP} from '../util/http-common';

export default {
  components: {
    DateRange,AccountSelectCombo,
    TransactionTable,
    meuBolsoLine
  },
  data() {
    return {
      chartData: {},
      title: "Running Balance",
      height: 300,
      fromDate: null,
      toDate: null,
      appendParams: {},
      allData: null
    };
  },
  mounted() {
    this.$refs.cashFlow_range.setRange(0, 6);
    this.search();
    this.fromDate = moment(this.$refs.cashFlow_range.fromDate).format("YYYY-MM-DD");
    this.toDate = moment(this.$refs.cashFlow_range.toDate).format("YYYY-MM-DD");
  },
  watch: {
    allData: {
      handler(newData, oldData) {
        this.getChartData();
      }
    }
  },
  methods: {
    getParams() {
      let params = {
        fromDate: this.fromDate,
        toDate: this.toDate
      };
      if (this.$refs.account_combo_all.getSelectedAccount() != "All") {
         params["bankName"] = this.$refs.account_combo_all.getSelectedAccount();
      }
      return params;
    },
    search() {
      this.fromDate = moment(this.$refs.cashFlow_range.fromDate).format("YYYY-MM-DD");
      this.toDate = moment(this.$refs.cashFlow_range.toDate).format("YYYY-MM-DD");
      HTTP
        .get("transactionsFiltered/?filter=" + JSON.stringify(this.getParams()))
        .then(response => {
          this.allData = response["data"]["data"];
        })
        .catch(function(error) {
          console.log(error);
        });
      this.$events.fire("transaction-filter-set", this.getParams());
    },
    createDataset(alabels, bank, allBankSerie, datasetsLength) {
      let values = [];
      let lastValue = 0;
      for (let x in alabels) {
        let runningDate = alabels[x];
        if (allBankSerie[runningDate] == undefined) {
          values.push(lastValue);
        } else {
          lastValue = allBankSerie[runningDate];
          values.push(allBankSerie[runningDate]);
        }
      }
      return {
        label: bank,
        fill: true,
        //backgroundColor: colors[datasetsLength % colors.length],
        borderColor: colors[datasetsLength % colors.length],
        data: values,
        showLine: true
      };
    },
    getChartData() {
      let datasets = [];
      let alabels = this.allData.map(x => moment(x.Date));
    
      alabels = alabels.sort(function(a, b) {
        return a - b;
      });

      alabels = alabels.map(function(m) {
        return m.format("YYYY-MM-DD");
      });
      alabels = Array.from(new Set(alabels));

      let groupedData = this.allData.reduce(function(r, a) {
        if (a.Active === "True") { //only active accounts
          r[a["BankName"]] = r[a["BankName"]] || {};
          let dateRunning = moment(a.Date).format("YYYY-MM-DD");
          r[a["BankName"]][dateRunning] = Math.round(a.RunningBalance);
        }
         return r;
      }, Object.create(null));

      let runningValues = [];
      for (let bank in groupedData) {
          datasets.push(
            this.createDataset(
              alabels,
              bank,
              groupedData[bank],
              datasets.length
            )
          );
        // }
      }
      this.chartData = {
        labels: alabels,
        datasets: datasets
      };
    }
  }
};
</script>

