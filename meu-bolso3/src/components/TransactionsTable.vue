<template>
<div>
  <v-card>
    <v-card-title>
      <v-dialog v-if="this.editedItem.BankName" v-model="dialog" max-width="700px">
        <template v-slot:activator="{ on }">
          <v-btn color="primary" dark class="mb-2" v-on="on">New Transaction</v-btn>
        </template>
        <transactionCRUD
          :typeTransaction="typeTransaction"
          :editedItem="editedItem"
          @close-dialog="closeDialog"
        ></transactionCRUD>
      </v-dialog>
      <v-spacer></v-spacer>
      <v-text-field v-model="search" append-icon="search" label="Search" single-line hide-details></v-text-field>
    </v-card-title>
    <v-card>
      <v-data-table :headers="headers" :items="allData" :search="search" :itemsPerPage="10"   
        show-select
        v-model="selected"
        item-key="BankName"
      >
        <template v-slot:item.Description="props">
          <v-edit-dialog :return-value.sync="props.item" @close="close(props.item)">
            {{ props.item.Description }}
            <template v-slot:input>
              <v-text-field
                v-model="props.item.Description"
                label="Edit"
                :rules="[max125chars]"
                single-line
                counter
              ></v-text-field>
            </template>
          </v-edit-dialog>
        </template>
        <template v-slot:item.Amount="props">
          <v-edit-dialog :return-value.sync="props.item" @close="close(props.item)">
            {{ props.item.Amount }}
            <template v-slot:input>
              <v-text-field
                v-model="props.item.Amount"
                :rules="[max25chars]"
                label="Edit"
                single-line
                counter
              ></v-text-field>
            </template>
          </v-edit-dialog>
        </template>
        <template v-slot:item.Date="props">
          <v-edit-dialog :return-value.sync="props.item" @close="close(props.item)">
            {{ props.item.Date }}
            <template v-slot:input>
              <v-text-field
                v-model="props.item.Date"
                :rules="[max25chars]"
                label="Edit"
                single-line
                counter
              ></v-text-field>
            </template>
          </v-edit-dialog>
        </template>
        <template v-slot:item.actions="{ item }">
          <v-icon small @click="editTransaction(item)">edit</v-icon>
          <v-icon small @click="addTransaction(item)">autorenew</v-icon>
          <v-icon small @click="onDelete(item)">delete</v-icon>
        </template>
      </v-data-table>
      <template v-slot:no-results>
        <v-alert
          :value="true"
          color="error"
          icon="warning"
        >Your search for "{{ search }}" found no results.</v-alert>
      </template>
      <v-snackbar v-model="snack" :timeout="1000" :color="snackColor">
        {{ snackText }}
        <v-btn flat @click="snack = false">Close</v-btn>
      </v-snackbar>
    </v-card>
  </v-card>
</div>
</template>

<script>
import { HTTP } from "../util/http-common";
import querystring from "querystring";
import TransactionCRUD from "./TransactionCRUD";
import moment from "moment";
import axios from "axios";

export default {
  props: {
    allData: Array,
    defaultDescriptionAdd: String,
    BankName: Array
  },
  components: {
    TransactionCRUD
  },
  data() {
    return {
      dialog: false,
      typeTransaction: "Add",
      search: "",
      snack: false,
      snackColor: "",
      snackText: "",
      selected: [],
      max125chars: v => v.length <= 125 || "Input too long!",
      max25chars: v => v.length <= 25 || "Input too long!",
      editedItem: {
        id: null,
        Description: null,
        Category_id: null,
        Currency: null,
        Date: null,
        BankName: null
      },
      selected: [],
      defaultItem: {
        Description: this.defaultDescriptionAdd,
        Category_id: 0,
        Currency: "EUR",
        Date: moment(new Date()).format("YYYY-MM-DD"),
        BankName: this.BankName
      },
      headers: [
        {
          text: "Band Name",
          value: "BankName",
          align: "left",
          sortable: false,
        },
        { text: "Type", value: "Type"}, 
        { text: "Category", value: "Category"}, 
        { text: "Subcategory", value: "SubCategory"},
        { text: "Description", value: "Description"}, 
        { text: "Currency", value: "Currency"}, 
        { text: "Amount", value: "Amount"}, 
        { text: "Date", value: "Date"}, 
        { text: "RunningBalance", value: "RunningBalance"}, 
        { text: "Actions", value: "actions"}
      ]
    };
  },
  mounted() {
    this.editedItem.Description = this.defaultDescriptionAdd;
  },
  watch: {
    BankName: {
      handler(newData, oldData) {
        this.editedItem.BankName = this.BankName[0];
      }
    }
  },
  methods: {
    isFuture(dataItem) {
      return dataItem.TransactionNumber === "Future";
    },
    saveTransaction(transaction_id, new_amount, new_date, Description) {
      HTTP.post(
        "transactions/",
        querystring.stringify({
          transaction_id: transaction_id,
          Description: Description,
          Date: new_date,
          Amount: new_amount
        })
      )
        .then(response => {
          this.snackColor = "success";
          this.snackText = "Data saved";
          this.$emit("refresh-transaction-table-data");
        })
        .catch(function(error) {
          this.snackColor = "fail";
          this.snackText = "Error";
        });
    },
    onDelete(data) {
      HTTP.delete("deleteTransaction/" + data.id, querystring.stringify())
        .then(response => {
          this.$emit("refresh-transaction-table-data");
        })
        .catch(function(error) {
          console.log(error.headers);
          console.log(error);
        });
    },
    close(item) {
      // this.snack = true;
      // this.snackColor = "success";
      // this.snackText = "Data saved";
      this.saveTransaction(item.id, item.Amount, item.Date, item.Description);
    },
    addTransaction(item) {
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
      this.typeTransaction = "Add";
    },
    editTransaction(item) {
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
      this.typeTransaction = "Edit";
    },
    closeDialog() {
      this.dialog = false;
      this.$emit("refresh-transaction-table-data");
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      }, 300);
    }
  }
};
</script>

<style>
.futuretransaction {
  color: grey;
}
</style>