<template>
  <div>
    <v-expansion-panel>
      <v-expansion-panel-content>
        <template v-slot:actions>
          <v-icon color="primary">$vuetify.icons.expand</v-icon>
        </template>
        <template v-slot:header>
          <div>Add Category</div>
        </template>
        <v-card>
          <v-form>
            <v-container>
              <v-layout>
                <v-flex xs12 md6>
                  <category-select ref="typecombos"></category-select>
                </v-flex>
                <v-flex xs12 md6>
                  <v-text-field v-model="description" :counter="20" label="Description" required></v-text-field>required
                </v-flex>

                <v-btn @click="add">Add</v-btn>
              </v-layout>
            </v-container>
          </v-form>
        </v-card>
      </v-expansion-panel-content>
    </v-expansion-panel>

    <v-card-title>
      <v-spacer></v-spacer>
      <v-text-field v-model="search" append-icon="search" label="Search" single-line hide-details></v-text-field>
    </v-card-title>
    <v-data-table :headers="headers" :items="allData" :search="search">
      <template v-slot:items="props">
        <td class="text-xs-left">{{ props.item.category.Type }}</td>
        <td class="text-xs-left">{{ props.item.category.Category }}</td>
        <td class="text-xs-left">{{ props.item.category.SubCategory }}</td>
        <td class="text-xs-left">
          <v-edit-dialog
            :return-value.sync="props.item"
            lazy
            @close="close(props.item)"
          >
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
        </td>
        <td class="justify-center layout px-0">
          <v-icon small @click="deleteItem(props.item)">delete</v-icon>
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
import CategorySelect from "./CategorySelect";
import querystring from "querystring";

export default {
  components: {
    CategorySelect
  },
  data() {
    return {
      search: "",
      snack: false,
      snackColor: "",
      snackText: "",
      max25chars: v => v.length <= 25 || "Input too long!",
      pagination: {},
      headers: [
        { text: "Type", value: "Type" },
        { text: "Category", value: "Category" },
        { text: "Subcategory", value: "SubCategory" },
        { text: "Description", value: "Description" }
      ],
      description: null,
      allData: []
    };
  },
  created() {
    this.getData();
  },
  methods: {
    getData() {
      HTTP({
        method: "get",
        url: "/categories/"
      })
        .then(response => {
          this.allData = response["data"]["data"];
          return this.allData.map(e => e.Type);
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    itemsTypes() {
      return [...new Set(this.allData.map(e => e.category.Type))];
    },
    itemsCategory() {
      return [...new Set(this.allData.map(e => e.category.Category))];
    },
    itemsSubCategory() {
      return [...new Set(this.allData.map(e => e.category.SubCategory))];
    },
    close(item) {
      this.snack = true;
      this.snackColor = "success";
      this.snackText = "Data saved";
      this.postCategory(item.id, item.category.id, item.Description);
    },
    deleteItem(data) {
      HTTP.delete("categories/" + data.id, querystring.stringify())
        .then(response => {
          this.getData();
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
      this.postCategory(
        null,
        this.$refs.typecombos.getSelectedCategoryId(),
        this.description
      );
    }
  }
};
</script>

<style>
.futuretransaction {
  color: grey;
}
</style>