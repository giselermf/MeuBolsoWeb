<template>

    <td v-if="isHeader">{{element}}</td>
    <td v-else >
      <input class="form-field-small" v-model="budgetValue" @change="saveBudget">
      <label>{{actualsValue}}</label>
    </td> 
</template>

<script>
export default {
  props: ["element", "isHeader", "categoryId", "Month", "Year"],
  components: {},
  data() {
    return {
      budgetValue: this.getBudget(),
      actualsValue: this.getActuals()
    };
  },
  methods: {
    saveBudget() {
      var axios = require("axios");
      var querystring = require("querystring");
      axios
        .post(
          "http://127.0.0.1:5000/budget/",
          querystring.stringify({
            id: this.getId(),
            Value: this.budgetValue,
            Month: this.Month,
            Year: this.Year,
            CategoryId: this.categoryId
          })
        )
        .catch(function(error) {
          console.log(error);
        });
    },
    getId() {
      if (this.element != undefined) {
        return this.element.id;
      }
    },
    getBudget() {
      if (this.element != undefined) {
        return this.element.Budget;
      }
      return 0;
    },
    getActuals() {
      if (this.element != undefined) return this.element.Actuals;
      return 0;
    }
  }
};
</script>
 