<template>
  <v-layout>
    <v-flex xs12 sm6 offset-sm3>
      <v-card>
        <v-layout>
          <v-flex xs12 md6>
            <v-text-field v-model="row.transaction2.BankName" label="Bank" :readonly="true"></v-text-field>
            <v-text-field
              v-model="row.transaction2.TransactionNumber"
              label="Number"
              :readonly="true"
            ></v-text-field>
            <v-text-field v-model="row.transaction2.Description" label="Desc" :readonly="true"></v-text-field>
            <v-text-field v-model="row.transaction2.Amount" label="Amount" :readonly="true"></v-text-field>
            <v-text-field v-model="row.transaction2.Date" label="Date" :readonly="true"></v-text-field>
            Catgory: {{row.transaction2.Type}} - {{row.transaction2.Category}} - {{row.transaction2.SubCategory}}
          </v-flex>
          <v-divider class="mx-3" inset vertical></v-divider>
          <v-flex xs12 md6>
            <v-text-field v-model="row.transaction1.BankName" label="Bank" :readonly="true"></v-text-field>
            <v-text-field
              v-model="row.transaction1.TransactionNumber"
              label="Number"
              :readonly="true"
            ></v-text-field>
            <v-text-field v-model="row.transaction1.Description" label="Desc" :readonly="true"></v-text-field>
            <v-text-field v-model="row.transaction1.Amount" label="Amount" :readonly="true"></v-text-field>
            <v-text-field v-model="row.transaction1.Date" label="Date" :readonly="true"></v-text-field>
            Catgory: {{row.transaction1.Type}} - {{row.transaction1.Category}} - {{row.transaction1.SubCategory}}
          </v-flex>
        </v-layout>
        <v-card-actions>
          <v-btn flat small color="orange" @click="onProcess(true, false)">Keep old</v-btn>
          <v-btn flat small color="orange" @click="onProcess(false, true)">Keep new</v-btn>
          <v-btn flat small color="orange" @click="onProcess(true, true)">Keep both</v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import { HTTP } from "../../util/http-common";
import querystring from "querystring";

export default {
  props: ["row"],
  data: function() {
    return {};
  },
  methods: {
    onProcess(oldT, newT) {
      HTTP.post(
        "ProcessReconciliation/",
        querystring.stringify({
          reconciliation_id: this.row.id,
          transaction1_id: this.row.transaction1.id,
          transaction1_keep: oldT,
          transaction2_id: this.row.transaction2.id,
          transaction2_keep: newT
        })
      )
        .then(response => {
          this.$events.fire("reconcilitions-refresh", response);
        })
        .catch(function(error) {
          console.log(error);
        });
    }
  }
};
</script>