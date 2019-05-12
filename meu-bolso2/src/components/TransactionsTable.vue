<template>
  <div>
    <v-card-title>
      <v-spacer></v-spacer>
      <v-text-field v-model="search" append-icon="search" label="Search" single-line hide-details></v-text-field>
    </v-card-title>
    <v-toolbar v-if="this.editedItem.BankName" flat color="white">
      <v-spacer></v-spacer>
      <v-dialog v-model="dialog" max-width="700px">
        <template v-slot:activator="{ on }">
          <v-btn color="primary" dark class="mb-2" v-on="on">New Transaction</v-btn>
        </template>
        <transaction-add :editedItem="editedItem" @close-dialog="closeDialog"></transaction-add>
      </v-dialog>
    </v-toolbar>
    <v-data-table :headers="headers" :items="allData" :search="search">
      <template v-slot:items="props">
        <td :class="getClass(props.item)">{{ props.item.BankName }}</td>
        <td :class="getClass(props.item)">{{ props.item.Type }}</td>
        <td :class="getClass(props.item)">{{ props.item.Category }}</td>
        <td :class="getClass(props.item)">{{ props.item.SubCategory }}</td>
        <td :class="getClass(props.item)">{{ props.item.Description }}</td>
        <td :class="getClass(props.item)">{{ props.item.Currency }}</td>
        <td :class="getClass(props.item)">
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
        <td :class="getClass(props.item)">
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
        <td :class="getClass(props.item)">{{ props.item.RunningBalance }}</td>
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
    BankName: String
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
      pagination: {},
      editedItem: {
        Description: null,
        Category_id: null,
        Currency: null,
        Date: null,
        BankName: null
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
          sortable: false
        },
        { text: "Type", value: "Type" },
        { text: "Category", value: "Category" },
        { text: "Subcategory", value: "SubCategory" },
        { text: "Description", value: "Description" },
        { text: "Currency", value: "Currency" },
        { text: "Amount", value: "Amount" },
        { text: "Date", value: "Date" },
        { text: "RunningBalance", value: "RunningBalance" },
        { text: "Actions", value: "Actions" }
      ]
    };
  },
  mounted() {
    this.editedItem.Description = this.defaultDescriptionAdd;
  },
  watch: {
    BankName: {
      handler(newData, oldData) {
        this.editedItem.BankName = this.BankName;
      }
    }
  },
  methods: {
    getClass(dataItem) {
      return dataItem.TransactionNumber === "Future"
        ? "text-xs-left futuretransaction"
        : "text-xs-left";
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