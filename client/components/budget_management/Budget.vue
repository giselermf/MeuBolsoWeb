<template>
      <div id="app" class="ui vertical segments" >
        <div class="ui  segment">         
            <div>
                <label class="form-label">Date:</label>
                <datepicker class="date-picker" v-model="fromDate" placeholder="from" :minimumView="'month'" :maximumView="'month'"></datepicker>
                <datepicker class="date-picker" v-model="toDate" placeholder="to" :minimumView="'month'" :maximumView="'month'"></datepicker>
                <button id="show-modal" @click="onSearch">Search</button>
            </div>
          </div>
        <div class="table-component__table-wrapper"  >
          <table>
              <thead>
              <tr>
                  <th v-for="col in columns" :key="col.Name" >{{col.Name}}</th>
              </tr>
              </thead>
              <tbody>
              <budget-row
                      v-for="row in tableData" :key="row.Name"
                      :row="row"
                      :columns="columns"
              ></budget-row>
              </tbody>
          </table>
          <button id="show-modal" @click="showModal = true">Add</button>
          <modal v-if="showModal" @close="showModal = false"></modal>
        </div>
    </div>
</template>

<script>
import BudgetRow from "./BudgetRow";
import Modal from "../util/CategoryModal.vue";
import Datepicker from "vuejs-datepicker";
import { addFilterParam } from "../util/Utils.js";
import moment from "moment";

export default {
  components: {
    BudgetRow,
    Modal,
    Datepicker
  },
  data() {
    return {
      headers: ["Type", "Category", "SubCategory", "category_id"],
      columns: [],
      tableFields: [],
      tableData: [],
      allData: null,
      showModal: false,
      fromDate: null,
      toDate: null
    };
  },
  created() {
    this.onSearch();
    this.fromDate = moment(new Date())
      .startOf("month").subtract(2, 'month')
      .format("YYYY-MM-DD");
    this.toDate = moment(new Date())
      .add(2, 'month')
     .format("YYYY-MM-DD");
  },
  mounted() {
    this.$events.$on("close-category-modal", eventData =>
      this.onModalClose(eventData)
    );
  },
  methods: {
    getParams() {
      let params = {};
      if (this.fromDate)
        params["fromDate"] = this.fromDate;
      if (this.toDate)
        params["toDate"] = this.toDate;
      return "?filter=" + JSON.stringify(params);
    },
    onSearch() {
      let axios = require("axios");
      let querystring = require("querystring");
      axios
        .get("http://127.0.0.1:5000/budget/" + this.getParams())
        .then(response => {
          this.allData = response["data"]["data"];
          this.setTableData();
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    onModalClose(eventData) {
      this.showModal = false;
      // check if the row is not already on the table.
      for (let row in this.tableData) {
        if (this.tableData[row].category_id == eventData.categoryId) return;
      }

      // add new row
      let newRow = {
        Type: eventData.selectedType,
        Category: eventData.selectedCategory,
        SubCategory: eventData.selectedSubCategory,
        category_id: eventData.categoryId
      };
      for (let col in this.columns) {
        let aCol = this.columns[col];
        if (!aCol.isHeader) {
          newRow[aCol.Name] = aCol;
        }
      }
      this.tableData.push(newRow);
    },
    getColumns() {
      // first column
      this.columns.push({ Name: "Type", isHeader: true });
      this.columns.push({ Name: "Category", isHeader: true });
      this.columns.push({ Name: "SubCategory", isHeader: true });

      // months/year columns
      let x = moment(this.fromDate);
      while (x <= moment(this.toDate)) {
        let month = x.month()+1;
        let year = x.year();
        let name = month + "/" + year;

        let newEntry = {Name: name, isHeader: false, Year: year, Month: month};
        if (!this.columns.find(function(obj) { return obj.Name === newEntry.Name;})) {
          this.columns.push(newEntry);
        }
        x = moment(x).add(1, "month");
      }
    },
    setTableData() {
      if (this.allData == null) return;

      //clean table
      this.tableData.splice(0, this.tableData.length);
      this.columns.splice(0, this.columns.length);

      this.getColumns();

      let groupedData = this.allData.reduce(function(r, a) {
        let groupName =
          a["Type"] + "/" + a["Category"] + "/" + a["SubCategory"];
        r[groupName] = r[groupName] || [];
        r[groupName].push(a);
        return r;
      }, Object.create(null));

      this.tableData = [];
      for (let e in groupedData) {
        let oneRow = {};
        oneRow["Type"] = groupedData[e][0]["Type"];
        oneRow["Category"] = groupedData[e][0]["Category"];
        oneRow["SubCategory"] = groupedData[e][0]["SubCategory"];
        oneRow["category_id"] = groupedData[e][0]["category_id"];
        for (let i in groupedData[e]) {
          let a = groupedData[e][i];
          oneRow[a.Month + "/" + a.Year] = a;
        }
        this.tableData.push(oneRow);
      }
    }
  }
};
</script>

<style>
.table-component__table-wrapper {
  min-height: 1300px;
}
</style>