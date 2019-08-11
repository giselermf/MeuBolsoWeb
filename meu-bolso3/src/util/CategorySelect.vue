<template>
  <div>
    <v-form>
      <v-layout>
        <v-flex xs12 md4>
          <v-select v-model="selectedType" :items="getTypes()" label="Type"></v-select>
        </v-flex>

        <v-flex xs12 md4>
          <v-select v-model="selectedCategory" :items="getCategories()" label="Category"></v-select>
        </v-flex>

        <v-flex xs12 md4>
          <v-select v-model="selectedSubCategory" :items="getSubCategories()" label="SubCategory"></v-select>
        </v-flex>
      </v-layout>
    </v-form>
  </div>
</template>
<script>
import { HTTP } from "../util/http-common";

export default {
  props: {
    Type: {
      type: String,
      default: ""
    },
    Category: {
      type: String,
      default: ""
    },
    SubCategory: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      type_data: null,
      category_data: null,
      allData: null,
      selectedType: null,
      selectedCategory: null,
      selectedSubCategory: null
    };
  },
  mounted() {
    this.selectedType = this.Type;
    this.selectedCategory = this.Category;
    this.selectedSubCategory = this.SubCategory;
    this.getFilterData();
  },
  watch: {
    selectedSubCategory: function(val) {
      this.$emit("selectedCategoryId", this.getSelectedCategoryId());
    }
  },
  methods: {
    getTypes() {
      if (this.type_data != null) return Object.keys(this.type_data);
    },
    getCategories() {
      if (this.type_data != null && this.type_data[this.selectedType] != null)
        return Array.from(this.type_data[this.selectedType]);
    },
    getSubCategories() {
      if (
        this.category_data != null &&
        this.category_data[this.selectedCategory] != null
      )
        return Array.from(this.category_data[this.selectedCategory]);
    },
    resetValues() {
      this.selectedType = null;
      this.selectedCategory = null;
      this.selectedSubCategory = null;
    },
    getFilterData() {
      HTTP.get("getFilterData/")
        .then(response => {
          this.allData = response["data"].data;
          this.processData();
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    getSelectedCategoryId() {
      if (
        this.selectedType &&
        this.selectedCategory &&
        this.selectedSubCategory
      ) {
        for (let e in this.allData) {
          if (
            this.allData[e]["Type"] == this.selectedType &&
            this.allData[e]["Category"] == this.selectedCategory &&
            this.allData[e]["SubCategory"] == this.selectedSubCategory
          )
            return this.allData[e].id;
        }
      } else return null;
    },
    processData() {
      this.type_data = this.allData.reduce(function(r, a) {
        r[a["Type"]] = r[a["Type"]] || new Set();
        r[a["Type"]].add(a["Category"]);
        return r;
      }, Object.create(null));
      this.category_data = this.allData.reduce(function(r, a) {
        r[a["Category"]] = r[a["Category"]] || new Set();
        r[a["Category"]].add(a["SubCategory"]);
        return r;
      }, Object.create(null));
    }
  }
};
</script>