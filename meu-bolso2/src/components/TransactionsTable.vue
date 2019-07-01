<template>
  <div>
    <v-layout row wrap>
      <v-flex xs12 sm6 md8>
        <v-spacer></v-spacer>
        <v-text-field v-model="search" append-icon="search" label="Search" single-line hide-details></v-text-field>
        <v-spacer></v-spacer>
      </v-flex>
      <v-flex xs12 sm6 md4>
        <v-dialog v-if="this.editedItem.BankName" v-model="dialog" max-width="700px">
          <template v-slot:activator="{ on }">
            <v-btn color="primary" dark class="mb-2" v-on="on">New Transaction</v-btn>
          </template>
          <transaction-add :editedItem="editedItem" @close-dialog="closeDialog"></transaction-add>
        </v-dialog>
      </v-flex>
    </v-layout>
    <v-data-table
      :headers="headers"
      :items="allData"
      :search="search"
      :pagination.sync="pagination"
    >
      <template v-slot:items="props">
        <td v-bind:class="{futuretransaction: isFuture(props.item)}">{{ props.item.BankName }}</td>
        <td v-bind:class="{futuretransaction: isFuture(props.item)}">{{ props.item.Type }}</td>
        <td v-bind:class="{futuretransaction: isFuture(props.item)}">{{ props.item.Category }}</td>
        <td v-bind:class="{futuretransaction: isFuture(props.item)}">{{ props.item.SubCategory }}</td>
        <td v-bind:class="{futuretransaction: isFuture(props.item)}">{{ props.item.Description }}</td>
        <td v-bind:class="{futuretransaction: isFuture(props.item)}">{{ props.item.Currency }}</td>
        <td >
          <v-edit-dialog :return-value.sync="props.item" lazy @close="close(props.item)">
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
        </td>
        <td >
          <v-edit-dialog :return-value.sync="props.item" lazy @close="close(props.item)">
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
        </td>
        <td v-bind:class="{futuretransaction: isFuture(props.item)}">{{ props.item.RunningBalance }}</td>
        <td class="justify-center layout px-0">
          <v-icon small class="mr-2" @click="addTransaction(props.item)">autorenew</v-icon>
          <v-icon small @click="onDelete(props.item)">delete</v-icon>
        </td>
      </template>

      <template v-slot:no-results>
        <v-alert
          :value="true"
          color="error"
          icon="warning"
        >Your search for "{{ search }}" found no results.</v-alert>
      </template>
    </v-data-table>

    <v-snackbar v-model="snack" :timeout="3000" :color="snackColor">
      {{ snackText }}
      <v-btn flat @click="snack = false">Close</v-btn>
    </v-snackbar>
  </div>
</template>

<script>
import { HTTP } from "../util/http-common";
import querystring from "querystring";
import TransactionAdd from "./TransactionAdd";
import moment from "moment";

export default {
  props: {
    allData: Array,
    defaultDescriptionAdd: String,
    BankName: Array
  },
  components: {
    TransactionAdd
  },
  data() {
    return {
      dialog: false,
      search: "",
      snack: false,
      snackColor: "",
      snackText: "",
      max25chars: v => v.length <= 25 || "Input too long!",
      editedItem: {
        Description: null,
        Category_id: null,
        Currency: null,
        Date: null,
        BankName: null
      },
      pagination: {
        rowsPerPage: -1
      },
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
          width: "8%"
        },
        { text: "Type", value: "Type" ,
          width: "1%"},
        { text: "Category", value: "Category" ,
          width: "1%"},
        { text: "Subcategory", value: "SubCategory" ,
          width: "1%"},
        { text: "Description", value: "Description" ,
          width: "8%"},
        { text: "Currency", value: "Currency" ,
          width: "2%"},
        { text: "Amount", value: "Amount" ,
          width: "1%"},
        { text: "Date", value: "Date" ,
          width: "2%"},
        { text: "RunningBalance", value: "RunningBalance" ,
          width: "1%"},
        { text: "Actions", value: "Actions" ,
          width: "1%"}
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
      return dataItem.TransactionNumber === "Future"
    },
    saveTransaction(transaction_id, new_amount, new_date) {
      HTTP.post(
        "transactions/",
        querystring.stringify({
          transaction_id: transaction_id,
          date: new_date,
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
          console.log(error);
        });
    },
    close(item) {
      this.snack = true;
      // this.snackColor = "success";
      // this.snackText = "Data saved";
      this.saveTransaction(item.id, item.Amount, item.Date);
    },
    addTransaction(item) {
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },
    closeDialog() {
      this.dialog = false;
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