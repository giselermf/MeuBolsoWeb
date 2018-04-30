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
        this.processData(response["data"]);
      })
      .catch(function(error) {
        console.log(error);
      });
  },
  methods: {
    onChangeType: function() {
      this.selectedCategory = null;
      this.selectedSubCategory = null;
    },
    onChangeCategory: function() {
      this.selectedSubCategory = null;
    },
    getTypes: function() {
      if (this.type_data != null) return Object.keys(this.type_data);
    },
    getCategories: function() {
      if (this.type_data != null && this.type_data[this.selectedType] != null)
        return Array.from(this.type_data[this.selectedType]);
    },
    getSubCategories: function() {
      if (
        this.category_data != null &&
        this.category_data[this.selectedCategory] != null
      )
        return Array.from(this.category_data[this.selectedCategory]);
    },
    processData: function(all_data) {
      this.type_data = all_data.reduce(function(r, a) {
        r[a["Type"]] = r[a["Type"]] || new Set();
        r[a["Type"]].add(a["Category"]);
        return r;
      }, Object.create(null));
      this.category_data = all_data.reduce(function(r, a) {
        r[a["Category"]] = r[a["Category"]] || new Set();
        r[a["Category"]].add(a["SubCategory"]);
        return r;
      }, Object.create(null));
    }
  }
};
</script>