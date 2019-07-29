<template>
  <v-card>
    <v-card-title>
      <v-dialog v-model="dialog" max-width="500px">
        <template v-slot:activator="{ on }">
          <v-btn color="primary" dark class="mb-2" v-on="on">New Item</v-btn>
        </template>
        <v-card>
          <v-card-text>
            <v-container grid-list-md>
              <category-select ref="typecombos"></category-select>
              <v-text-field v-model="editedItem.Description" label="Description" required></v-text-field>
            </v-container>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
            <v-btn color="blue darken-1" text @click="add">Save</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-spacer></v-spacer>
      <v-text-field v-model="search" append-icon="search" label="Search" single-line hide-details></v-text-field>
    </v-card-title>

    <v-data-table :headers="headers" :items="allData" :search="search" dense :items-per-page="20">
      
      <template v-slot:item.Description="props">
        
        <v-edit-dialog :return-value.sync="props.item" @close="save(props.item)">
          {{ props.item.Description }}
          <template v-slot:input>
            <v-text-field
              v-model="props.item.Description"
              :rules="[max25chars]"
              label="Edit"
              single-line
              counter
            ></v-text-field>
          </template>
        </v-edit-dialog>
      </template>

      <template v-slot:item.action="{ item }">
        <v-icon small @click="deleteItem(item)">delete</v-icon>
      </template>
    </v-data-table>

    <v-snackbar v-model="snack" :timeout="1000" :color="snackColor">
      {{ snackText }}
      <v-btn text @click="snack = false">Close</v-btn>
    </v-snackbar>
  </v-card>
</template>


<script>
import { HTTP } from "../util/http-common";
import querystring from "querystring";
import CategorySelect from "../util/CategorySelect";

export default {
  components: {
    CategorySelect
  },
  data() {
    return {
      snack: false,
      search: "",
      snackColor: "",
      snackText: "",
      max25chars: v => v.length <= 25 || "Input too long!",
      pagination: {},
      allData: [],
      dialog: false,
      editedItem: {
        Type: "",
        Category: "",
        Subcategory: "",
        Description: ""
      },
      headers: [
        { text: "Type", value: "category.Type" },
        { text: "Category", value: "category.Category" },
        { text: "Subcategory", value: "category.SubCategory" },
        { text: "Description", value: "Description" },
        { text: "Actions", value: "action", sortable: false }
      ]
    };
  },
  mounted() {
    this.getData();
  },
  methods: {
    getData() {
      console.log("get data");
      HTTP.get("/categories/")
        .then(response => {
          this.allData = response["data"]["data"];
          return this.allData.map(e => e.Type);
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    postCategory(id, selectedCategoryId, description) {
      if (selectedCategoryId == null) return;
      HTTP.post(
        "categories/",
        querystring.stringify({
          id: id,
          selectedCategoryid: selectedCategoryId,
          description: description
        })
      )
        .then(response => {
          this.getData();
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    add() {
      if (
        this.editedItem.Description != undefined &&
        this.$refs.typecombos.getSelectedCategoryId() != undefined
      ) {
        this.snack = true;
        this.snackColor = "success";
        this.snackText = "Data added";
        this.postCategory(
          null,
          this.$refs.typecombos.getSelectedCategoryId(),
          this.editedItem.Description
        );
      }
      this.dialog = false;
    },
    save(item) {
      this.snack = true;
      this.snackColor = "success";
      this.snackText = "Data saved";
      this.dialog = false;
      this.postCategory(item.id, item.category.id, item.Description);
    },
    close() {
      this.dialog = false;
    },
    deleteItem(data) {
      HTTP.delete("categories/" + data.id, querystring.stringify())
        .then(response => {
          this.getData();
        })
        .catch(function(error) {
          console.log(error);
        });
    }
  }
};
</script>