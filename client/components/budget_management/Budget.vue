<template>
    <div class="table-component__table-wrapper">
      <table>
          <thead>
          <tr>
              <th v-for="col in columns" :key="col" >{{col}}</th>
          </tr>
          </thead>
          <tbody>
          <table-row
                  v-for="row in tableData" :key="row"
                  :row="row"
                  :columns="columns"
                  :firstColumnLabel="firstColumnLabel"
          ></table-row>
          </tbody>
      </table>
    </div>
</template>

<script>
import TableColumn from "./TableColumn";
import TableRow from "./TableRow";
export default {
  components: {
    TableRow
  },
  data() {
    return {
      firstColumnLabel: "Category/SubCategory",
      columns: null,
      tableFields: [],
      tableData: [],
      allData: null,
    };
  },
  created() {
    this.getData();
  },
  methods: {
    getData() {
      let axios = require("axios");
      let querystring = require("querystring");
      axios
        .get("http://127.0.0.1:5000/budget/")
        .then(response => {
          this.allData = response["data"]["data"];
          this.setTableData();
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    setTableData() {
      if (this.allData == null) return;
      this.columns =  [this.firstColumnLabel].concat(Array.from(new Set(this.allData.map(a => a["Month"] + "/" + a["Year"]))));

      let groupedData = this.allData.reduce(function(r, a) {
        r[a["Category"] + "/" + a["SubCategory"]] =
          r[a["Category"] + "/" + a["SubCategory"]] || [];
        r[a["Category"] + "/" + a["SubCategory"]].push(a);
        return r;
      }, Object.create(null));

      this.tableData = [];
      for (let e in groupedData) {
        let oneRow = {};
        oneRow[this.firstColumnLabel] = e;
        for (let i in groupedData[e]) {
          let a = groupedData[e][i];
          oneRow[ a.Month + "/" + a.Year] = a
        }
        this.tableData.push(oneRow)
      }
    }
  }
};
</script>