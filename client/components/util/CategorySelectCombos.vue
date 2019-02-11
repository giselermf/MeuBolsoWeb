<template>
  <div>
    <div class="field is-horizontal" >
        <div class="field-label">
            <label class="label">Type</label>
        </div>
        <div class="field-body">
            <div class="field is-grouped">
                <select class="select" v-model="selectedType" v-on:change="onChangeType" >
                  <option v-for="type in getTypes()" v-bind:key="type" v-bind:value="type">
                      {{ type }}
                  </option>
              </select>
        </div></div>
    </div>
    
    <div>
      <div v-if="selectedSubCategory=='Transfer'" >
        <account-select-combo ref="account_combo" ></account-select-combo>
      </div>
    </div>
    
    <div  v-if="selectedSubCategory!='Transfer'" class="field is-horizontal" >
        <div class="field-label">
            <label class="label">Category</label>
        </div>
        <div class="field-body">
            <div class="field is-grouped">
              <select class="select" v-model="selectedCategory" v-on:change="onChangeCategory">
                  <option v-for="category in getCategories()" v-bind:key="category" v-bind:value="category">
                      {{ category }}
                  </option>
              </select>
        </div></div>
    </div>
    <div v-if="selectedSubCategory!='Transfer'" class="field is-horizontal" >
        <div class="field-label">
            <label class="label">SubCategory</label>
        </div>
        <div class="field-body">
            <div class="field is-grouped">
              <select class="select" v-model="selectedSubCategory">
                  <option v-for="subcategory in getSubCategories()" v-bind:key="subcategory" v-bind:value="subcategory">
                      {{ subcategory }}
                  </option>
              </select>
        </div></div>
    </div>
  </div>  
</template>
<script>
import AccountSelectCombo from "../util/AccountSelectCombo.vue"

export default { 
  components: {
      AccountSelectCombo
  },
  data() {
    return {
      type_data: null,
      category_data: null,
      selectedType: null,
      selectedCategory: null,
      selectedSubCategory: null,
      allData: null
    };
  },
  mounted() {
    this.getFilterData();
  },
  methods: {
    onChangeType() {
      this.selectedCategory = null;
      this.selectedSubCategory = null;
    },
    onChangeCategory() {
      this.selectedSubCategory = null;
    },
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
    setValues(type, category, subcategory) {
      console.log('set values in combo', type, category, subcategory)
      this.selectedType = type;
      this.selectedCategory = category;
      this.selectedSubCategory = subcategory;
    },
    getSelectedType() {
      return this.selectedType;
    },
    getSelectedCategory() {
      return this.selectedCategory;
    },
    getSelectedSubCategory() {
      return this.selectedSubCategory;
    },
    getSelectedTransferAccount() {
      return this.$refs.account_combo.getSelectedAccount();
    },
    getFilterData() {
      var axios = require("axios");
      var querystring = require("querystring");
      axios
      .get("http://127.0.0.1:5000/getFilterData/")
      .then(response => {
        this.allData = response["data"].data;
        this.processData();
      })
      .catch(function(error) {
        console.log(error);
      });
    },
    getSelectedTransferBank() {
      retr=y
    },
    getSelectedCategoryId() {
      if (
        this.selectedType != null &&
        this.selectedCategory != null &&
        this.selectedSubCategory != null
      ) {
        for (let e in this.allData) {
          if (
            this.allData[e]["Type"] == this.selectedType &&
            this.allData[e]["Category"] == this.selectedCategory &&
            this.allData[e]["SubCategory"] == this.selectedSubCategory
          )
            return this.allData[e].id;
        }
      }
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