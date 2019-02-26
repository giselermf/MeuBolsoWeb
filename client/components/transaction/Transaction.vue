<template>
  <div id="app" class="ui vertical segments">
    <div id="app" class="ui horizontal segments">
      <div class="ui segment four wide column">
        <transaction-search></transaction-search>
      </div>
      <div class="ui segment eight wide column">

        <div class="tabs help-tabs">
          <ul>
            <li :class="[ tab_value === 'table' ? 'is-active' : '']">
              <a @click="tab_value='table'">Transaction Table</a>
            </li>
            <li :class="[ tab_value === 'flow' ? 'is-active' : '']">
              <a @click="tab_value='flow'">Cash Flow</a>
            </li>
          </ul>
        </div>

        <div class="box help-content">
          <code v-if="tab_value ==='table'">
              <select v-model="grouper">
                <option disabled value>Please select one</option>
                <option>Type</option>
                <option>Category</option>
                <option>SubCategory</option>
              </select>
              <over-month-with-table
                :height="300"
                :allData="allData"
                :show-table="true"
                :grouper="grouper"
              ></over-month-with-table>
          </code>
          <code v-if="tab_value ==='flow'">
              <meu-bolso-line :height=300 :chartData="chartData" :title="title" xLabel="Date" datasetLabel="BankName"></meu-bolso-line>
          </code>
      </div>
      </div>
    </div>

    <div class="ui segment">
      <transaction-table :params="appendParams"></transaction-table>
    </div>
  </div>
</template>

<script>
import TransactionSearch from "./TransactionSearch.vue";
import TransactionTable from "./TransactionTable.vue";
import OverMonthWithTable from "./OverMonthBarWithTable.vue";
import { HTTP } from "../util/http-common";
import meuBolsoLine from "../charts/meuBolsoLine.js";
import moment from "moment";
import { colors } from "../util/Utils.js";

export default {
  components: {
    TransactionSearch,
    TransactionTable,
    OverMonthWithTable,
    meuBolsoLine
  },
  data() {
    return {
      appendParams: {},
      allData: null,
      grouper: "Category",
      tab_value: "table",
      title: "Running Balance",
      chartData: {},
    };
  },
  created() {
    this.getData();
    this.$events.$on("transaction-filter-set", eventData =>
      this.onFilterSet(eventData)
    );
  },
  watch: {
    allData: {
      handler(newData, oldData) {
        this.getChartData();
      }
    }
  },
  methods: {
    getData() {
      if (this.getFilterParam() != "") {
        //don't call without filter
        HTTP({
          method: "get",
          url: "transactionsFiltered/" + this.getFilterParam()
        })
          .then(response => {
            this.allData = response["data"]["data"];
          })
          .catch(function(error) {
            console.log(error);
          });
      }
    },
    getFilterParam() {
      if (this.appendParams.filter == undefined) return "";
      else return "?filter=" + JSON.stringify(this.appendParams.filter);
    },
    onFilterSet(filterParams) {
      this.appendParams.filter = filterParams;
      this.getData();
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