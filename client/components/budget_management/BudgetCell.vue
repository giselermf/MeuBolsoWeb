<template>
    <td  style="width: 250px;" v-if="isHeader">{{element}}</td>
    <td v-else >
      <div class="columns">
        <p  v-if="isTotal" class="column is-one-quarter total">
            <label>{{budgetValue}}</label>
        <p v-else class="column is-one-third">
          <input v-bind:class="budgetClass" v-model="budgetValue" @change="saveBudget">
        </p>
        <p  v-if="isTotal" class="column is-one-third">
            <label>{{actualsValue}}</label>
        <p v-else  class="column is-one-third">  
            <input v-bind:class="actualsClass" type="text" v-model="actualsValue" disabled>
        </p>
        <p  v-if="!isTotal" class="column is-one-third">
          <progress :class="progressBarClass" style="margin-top: 10px;" :value="progressValue" :max="100"></progress>
        </p>
      </div>
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
      isTotal: this.getIsTotal(),
      progressValue: null,
      progressBarClass: null
    };
  },
  computed: {
    budgetClass: function() {
      return {
        negative: this.budgetValue < 0,
        "input budget-cell": true
      };
    },
    actualsClass: function() {
      return {
        negative: this.actualsValue < 0,
        "input": true
      };
    }
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
        ).then(response => {
          this.$events.fire("search-budget", response);
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    getId() {
      if (this.element != undefined) {
        return this.element.id;
      }
    },
    getIsTotal() {
      if (this.element != undefined && this.element.isTotal != "") {
        return this.element.isTotal;
      }
      return false;
    },
   getBudget() {
      if (this.element != undefined && this.element.Budget != "") {
        return parseInt(this.element.Budget);
      }
      return 0;
    },
    getActuals() {
      if (this.element != undefined && this.element.Actuals != "")
        return parseInt(this.element.Actuals);
      return 0;
    },
    getProgress() {
      if (this.getBudget() != 0)
        this.progressValue =
          Math.abs(this.getActuals() / this.getBudget()) * 100;
      else this.progressValue = 200;
      this.getProgressBarClass();
    },
    getProgressBarClass() {
      this.progressBarClass = "progress is-small ";
      if (this.progressValue > 100 && this.getBudget() <= 0) this.progressBarClass += "is-danger";
      else if (this.progressValue > 100 && this.getBudget() > 0)  this.progressBarClass += "is-success";
      else if (this.progressValue > 50) this.progressBarClass += "is-warning";
      else this.progressBarClass += "is-success";
    }
  }
};
</script>
 
 <style>
.budget-cell {
  max-width: 50%;
  min-width: 80px;
}

.label-cell {
  margin-top: 10px
}
.negative {
  color: red;
}

.ui.table tfoot
{
    border-top: 2px solid black;
    
}
</style>