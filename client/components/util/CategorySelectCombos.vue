<script>
export default {
  data() {
    return {
      type_data: null,
      category_data: null,
      selectedType: null,
      selectedCategory: null,
      selectedSubCategory: null
    };
  },
  mounted() {
    var axios = require("axios");
    var querystring = require("querystring");
    axios
      .get("http://127.0.0.1:5000/getFilterData/")
      .then(response => {
        this.allData = response["data"];
        this.processData();
        this.setInitalValues();
      })
      .catch(function(error) {
        console.log(error);
      });
  },
  methods: {
    setInitalValues() {
      if (this.type_data != null && this.selectedType == null) {
        this.selectedType = Object.keys(this.type_data)[0];
        if (this.category_data != null && this.selectedCategory == null) {
          this.selectedCategory = Object.keys(this.category_data)[0];
          if (this.selectedSubCategory == null) {
            this.selectedSubCategory = Array.from(this.category_data[
              this.selectedCategory
            ])[0];
          }
        }
      }
    },
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