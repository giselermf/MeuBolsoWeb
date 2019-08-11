<template>
  <div>
    <v-btn color="primary" @click="recategorize">Recategorize</v-btn>
    <v-divider class="mx-4" inset vertical></v-divider>
    <v-btn color="primary" @click="newItem">New Item</v-btn>

    <v-dialog v-model="dialogCR" max-width="500px">
      <v-card>
        <v-card-text>
          <v-container grid-list-md>
            <category-select :editedItem="editedItem.category" ref="typecombos"></category-select>
            <v-text-field v-model="editedItem.Description" label="Description" required></v-text-field>
          </v-container>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="close">Cancel</v-btn>
          <v-btn color="primary" text @click="add">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-spacer></v-spacer>
    <v-text-field v-model="search" append-icon="search" label="Search" single-line hide-details></v-text-field>

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
        <v-icon small @click="updateCategory(item)">edit</v-icon>
        <v-icon small @click="deleteItem(item)">delete</v-icon>
      </template>
    </v-data-table>

    <v-snackbar v-model="snack" :timeout="1000" :color="snackColor">
      {{ snackText }}
      <v-btn color="primary" text @click="snack = false">Close</v-btn>
    </v-snackbar>
  </div>
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
      dialogCR: false,
      editedItem: {
        id: null,
        category: {
          Type: "",
          Category: "",
          Subcategory: ""
        },
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
    recategorize() {
      HTTP.post("updateCategories/", {})
        .then(response => {
          console.log("recategorize");
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    newItem() {
      this.editedItem = {
        id: null,
        category: {
          Type: "",
          Category: "",
          Subcategory: ""
        },
        Description: ""
      };
      this.dialogCR = true;
    },
    updateCategory(item) {
      console.log("here", item);
      this.editedItem = item;
      // this.editedItem = item;
      // this.editedItem.Category = item.Category;
      // this.editedItem.Subcategory = item.Subcategory;
      // this.editedItem.Description = item.Description;
      // this.$refs.typecombos.setValues(item.Type, item.Category, item.Subcategory)
      this.dialogCR = true;
    },
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
      console.log(this.allData);
      console.log("post", this.editedItem);
      if (
        this.editedItem.Description != undefined &&
        this.$refs.typecombos.getSelectedCategoryId() != undefined
      ) {
        this.snack = true;
        this.snackColor = "success";
        this.snackText = "Data added";
        this.postCategory(
          this.editedItem.id,
          this.$refs.typecombos.getSelectedCategoryId(),
          this.editedItem.Description
        );
      }
      this.dialogCR = false;
    },
    save(item) {
      this.snack = true;
      this.snackColor = "success";
      this.snackText = "Data saved";
      this.dialogCR = false;
      this.postCategory(item.id, item.category.id, item.Description);
    },
    close() {
      this.dialogCR = false;
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