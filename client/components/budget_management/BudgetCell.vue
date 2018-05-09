<template>

    <td v-if="isHeader">{{element}}</td>
    <td v-else >
      <input class="input budget-cell" v-model="budgetValue" @change="saveBudget">
      <label>{{actualsValue}}</label>
      <progress :class="progressBarClass" :value="progressValue" :max="100"></progress>

    </td> 
</template>

<script>

export default {
  props: ["element", "isHeader", "categoryId", "Month", "Year"],
  components: {},
  data() {
    return {
      budgetValue: this.getBudget(),
      actualsValue: this.getActuals(),
      progressValue: null,
      progressBarClass: null
    };
  },
  created() {
    this.getProgress();
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
        return parseInt(this.element.Budget);
      }
      return 0;
    },
    getActuals() {
      if (this.element != undefined) return parseInt(this.element.Actuals);
      return 0;
    },
    getProgress() {
      if (this.getBudget() != 0) this.progressValue = Math.abs(this.getActuals()/this.getBudget())*100;
      else this.progressValue = 0;
      this.getProgressBarClass();
    },
    getProgressBarClass() {
      this.progressBarClass = 'progress is-small ';
      if (this.progressValue > 70) this.progressBarClass += 'is-danger';
      else if (this.progressValue > 50) this.progressBarClass += 'is-warning';
      else this.progressBarClass += 'is-success';
    }
  }
};
</script>
 
 <style>
 .budget-cell {
   max-width: 50%
 }
 </style>