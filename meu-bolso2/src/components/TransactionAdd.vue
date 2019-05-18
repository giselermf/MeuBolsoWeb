<template>
  <v-card>
    <v-card-title>
      <span class="headline">New Transaction</span>
    </v-card-title>
    <v-card-text>
      <v-flex>
        <v-text-field
          v-model="editedItem.BankName"
          :counter="100"
          :disabled="true"
          abel="BankName *"
          required
        ></v-text-field>
      </v-flex>
      <v-flex>
        <category-select ref="typecombos"></category-select>
      </v-flex>
      <v-flex>
        <v-text-field
          v-model="editedItem.Description"
          :counter="100"
          label="Description *"
          required
        ></v-text-field>
      </v-flex>
      <v-layout wrap>
        <v-flex xs12 md3>
          <v-text-field v-model="editedItem.Amount" :counter="10" label="Amount *" required></v-text-field>
        </v-flex>
        <v-flex xs12 md6>
          <v-combobox
            v-model="editedItem.Currency"
            :items="['USD', 'EUR']"
            label="Currency *"
            required
          ></v-combobox>
        </v-flex>
      </v-layout>
      <v-layout wrap>
        <v-flex xs12 md3>
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
                v-model="editedItem.Date"
                label="Date *"
                prepend-icon="event"
                readonly
                v-on="on"
              ></v-text-field>
            </template>
            <v-date-picker v-model="editedItem.Date" @input="menuDF = false" required></v-date-picker>
          </v-menu>
        </v-flex>
        <v-flex xs12 md3>
          <v-text-field v-model="numberOccurrencies" :counter="2" label="Occurrencies *" required></v-text-field>
        </v-flex>
        <v-flex xs12 md6>
          <v-combobox
            v-model="frequency"
            :items="['Weekly', 'Monthly', 'Quartely', 'Yearly']"
            label="Frequency *"
            required
          ></v-combobox>
        </v-flex>
      </v-layout>
    </v-card-text>

    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="blue darken-1" flat @click="closeDialog">Cancel</v-btn>
      <v-btn color="blue darken-1" flat @click="onAddFutureTransactions">Add</v-btn>
    </v-card-actions>
  </v-card>
</template>
<script>
import CategorySelect from "../util/CategorySelect";
import moment from "moment";
import { HTTP } from "../util/http-common";
import querystring from "querystring";

export default {
  components: {
    CategorySelect
  },
  props: {
    editedItem: {
      Description: String,
      Category_id: Number,
      Amount: {
        type: Number,
        default: 0
      },
      Currency: {
        type: Date,
        default: "EUR"
      },
      Date: {
        type: Date,
        default: moment(new Date()).format("YYYY-MM-DD")
      },
      BankName: {
        type: String,
        required: true
      }
    }
  },
  mounted() {
    this.$refs.typecombos.setValues(
      this.editedItem.Type,
      this.editedItem.Category,
      this.editedItem.SubCategory
    );
  },
  data() {
    return {
      frequency: "Monthly",
      numberOccurrencies: 1
    };
  },
  methods: {
    postTransactions(transaction_date) {
      if (
        this.editedItem.BankName &&
        this.editedItem.Amount &&
        this.$refs.typecombos.getSelectedCategoryId()
      ) {
        HTTP.post(
          "transactions/",
          querystring.stringify({
            category_id: this.$refs.typecombos.getSelectedCategoryId(),
            Description: this.editedItem.Description,
            Date: transaction_date,
            Currency: this.editedItem.Currency,
            Amount: this.editedItem.Amount,
            BankName: this.editedItem.BankName
          })
        )
          .then(response => {
            this.getData();
          })
          .catch(function(error) {
            console.log(error);
          });
      } else {
        console.log("no values to save transactions");
      }
    },
    closeDialog() {
      this.$emit("close-dialog");
    },
    onAddFutureTransactions() {
      let transaction_date = this.editedItem.Date;

      for (let i = 0; i < this.numberOccurrencies; i++) {
        this.postTransactions(transaction_date);
        if (this.frequency == "Monthly") {
          transaction_date = moment(transaction_date)
            .add(1, "months")
            .format("YYYY-MM-DD");
        }
        if (this.frequency == "Weekly") {
          transaction_date = moment(transaction_date)
            .add(7, "days")
            .format("YYYY-MM-DD");
        }
        if (this.frequency == "Quartely") {
          transaction_date = moment(transaction_date)
            .add(3, "years")
            .format("YYYY-MM-DD");
        }
        if (this.frequency == "Yearly") {
          transaction_date = moment(transaction_date)
            .add(1, "months")
            .format("YYYY-MM-DD");
        }
      }
      this.$emit("close-dialog");
    }
  }
};
</script>