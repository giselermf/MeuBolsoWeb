<template>
  <div id="app" class="ui vertical segments" >
    <div id="app" class="ui vertical segments" >
      <div class="field is-grouped">
        <p class="control">
          <date-range ref="cashFlow_range" minimumView="month"></date-range>            
        </p>
        <p class="control">
          <button class="button is-link" @click="search()" >Search</button>
        </p>
      </div>
    </div>
    <div id="app" class="ui vertical segments" style="overflow-x: auto;">
      <div class="ui vertical segment"  >
        <table  class="vuetable ui blue selectable celled stackable attached table">
          <thead>
            <tr>
                <th v-for="col in columns" :key="col.Name" >{{col.Name}} 
                  <a v-if="col.isHeader != true" class="is-link" @click="copyFromPrevious(col.Month, col.Year)">Copy</a></th>
                
            </tr>
          </thead>
            <tbody>
              <budget-row
                      v-for="row in tableDataIncome" :key="row.categoryId"
                      :row="row"
                      :columns="columns" 
              ></budget-row>
              <budget-row
                      v-for="row in tableDataExpense" :key="row.categoryId"
                      :row="row"
                      :columns="columns"  
              ></budget-row>
              <budget-row
                    v-for="row in grandTotal" :key="row.categoryId"
                    :row="row"
                    :columns="columns"
              ></budget-row>
            </tbody>
        </table>
    </div>
    <div class="field is-grouped is-grouped-centered" style="padding-top: 10px;" >
        <button class="button is-link" @click="showModal = true">Add</button>
    </div>
    <modal v-if="showModal" @close="showModal = false"></modal>
  </div>
</div>
</template>

<script>
import BudgetRow from "./BudgetRow";
import Modal from "./CategoryModal.vue";
import { addFilterParam } from "../util/Utils.js";
import DateRange from "../util/DateRange.vue";
import moment from "moment";
import {HTTP} from '../util/http-common';
import querystring  from "querystring"

export default {
  components: {
    BudgetRow,
    Modal,
    DateRange
  },
  data() {
    return {
      headers: ["Category & SubCategory", "category_id"],
      columns: [],
      tableFields: [],
      tableDataIncome: [],
      tableDataExpense: [],
      grandTotal: [],
      showModal: false,
      allData: null
    };
  },
  watch: {
    allData: function(val) {
      this.setTableData();
    },
  },
  mounted() {
    this.$refs.cashFlow_range.setRange(0, 4);
    this.search();
    this.$events.$on("search-budget", eventData => { this.search(); });
    this.$events.$on("close-category-modal", eventData => this.onModalClose(eventData)
    );
  },
  methods: {
    search() {
      HTTP.get("budget/" + this.getParams())
        .then(response => {
          this.allData = response["data"]["data"];
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    getParams() {
      return "?filter=" + this.$refs.cashFlow_range.getDateParams();
    },
    addIfNotThereYet(newRow, table) {
      for (let row in table) {
        if (table[row].category_id == newRow.category_id) return;
      }
      table.push(newRow);
    },
    onModalClose(eventData) {
      this.showModal = false;

      if (eventData.categoryId == null) return;

      // add new row
      let newRow = {};
      newRow["Category & SubCategory"] = eventData.selectedCategory + " & " + eventData.selectedSubCategory;
      newRow["category_id"] = eventData.categoryId;
      if (eventData.selectedType == "Income") {
         this.addIfNotThereYet(newRow, this.tableDataIncome);
      } else {
         this.addIfNotThereYet(newRow, this.tableDataExpense);
      };
    },
    getColumns() {
      // first column
      this.columns.push({ Name: "Category & SubCategory", isHeader: true });
      // months/year columns
      let x = moment(this.$refs.cashFlow_range.fromDate);
      while (x <= moment(this.$refs.cashFlow_range.toDate)) {
        let month = x.month() + 1;
        let year = x.year();
        let name = month + "/" + year;
        let newEntry = {
          Name: name,
          isHeader: false,
          Year: year,
          Month: month
        };
        if (
          !this.columns.find(function(obj) {
            return obj.Name === newEntry.Name;
          })
        ) {
          this.columns.push(newEntry);
        }
        x = moment(x).add(1, "month");
      }
    },
    setTableData() {
      if (this.allData == null) return;

      //clean table
      this.tableDataIncome.splice(0, this.tableDataIncome.length);
      this.tableDataExpense.splice(0, this.tableDataExpense.length);

      this.columns.splice(0, this.columns.length);

      this.getColumns();
      let groupedData = this.allData.reduce(function(r, a) {
        let groupName =
          a["Type"] + "/" + a["Category"] + "/" + a["SubCategory"];
        r[groupName] = r[groupName] || [];
        r[groupName].push(a);
        return r;
      }, Object.create(null));


      this.tableDataIncome = [];
      this.tableDataExpense = [];
      for (let e in groupedData) {
        let oneRow = {};
        oneRow["Category & SubCategory"] = groupedData[e][0]["Category"] + " & " + groupedData[e][0]["SubCategory"];
        oneRow["category_id"] = groupedData[e][0]["category_id"];
        for (let i in groupedData[e]) {
          let a = groupedData[e][i];
          oneRow[a.Month + "/" + a.Year] = a;
        }
        if (groupedData[e][0]["Type"] == "Income") {
          this.tableDataIncome.push(oneRow);
        } else {
          this.tableDataExpense.push(oneRow);
        }
      }
      this.grandTotal = [this.allData.reduce(function (r, a) {
        r[a["Year"] + "/" + a["Month"]] = r[a["Year"] + "/" + a["Month"]] || {Type:"Total", Month:a["Month"], Year:a["Year"], Amount: 0, Actuals:0, isTotal: true };
        r[a["Year"] + "/" + a["Month"]].Amount += a.Amount;
        r[a["Year"] + "/" + a["Month"]].Actuals += a.Actuals;
        r["Category & SubCategory"] = "Total";
        return r;
      }, Object.create(null))];
    },
    copyFromPrevious(Month, Year) {
       HTTP.post(
          "copyBudget/",
          querystring.stringify({
            Month: Month,
            Year: Year,
          })
        )
        .then(response => {
          this.$events.fire("search-budget", response);
        })
        .catch(function(error) {
          console.log(error);
        });
    }
  }
};
</script>

<style>


.ui.table tfoot
{
  border-top: 2px solid black;
  background-color: #F9FAFB;
  font-weight: 700;
  vertical-align: middle;
  height: 44px
}
</style>