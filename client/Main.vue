<template>
  <div class="container">
    <div class="columns">
      <div class="column is-12">
          <div class="tabs help-tabs">
              <ul>
                  <li :class="[ tab_value === 'home' ? 'is-active' : '']"><a @click="tab_value='home'">Home</a>
                  </li>
                  <li :class="[ tab_value === 'records' ? 'is-active' : '']"><a @click="tab_value='records'">Bank Records</a></li>
                  <li :class="[ tab_value === 'categories' ? 'is-active' : '']"><a @click="tab_value='categories'">Categories</a></li>
                  <li :class="[ tab_value === 'budget' ? 'is-active' : '']"><a @click="tab_value='budget'">Budget</a></li>
                  <li :class="[ tab_value === 'process' ? 'is-active' : '']"><a @click="tab_value='process'">Process Data</a></li>
              </ul>
          </div>
        </div>
      </div>

      <div>
          <div v-if="tab_value === 'home' ">
              <main-dashboard></main-dashboard>
          </div>
          <div v-if="tab_value ==='records'">
              <transaction></transaction>
          </div>
          <div v-if="tab_value ==='categories'">
              <category></category>
          </div>
          <div v-if="tab_value ==='budget'">
              <budget></budget>
          </div>
          <div v-if="tab_value ==='process'">
              <process-data></process-data>
          </div>
      </div>
     </div>
</template>

<script>
import MainDashboard from "./components/main_dashboard/MainDashboard.vue";
import Category from "./components/data_management/CategoryEdit.vue";
import Transaction from "./components/data_management/Transaction.vue";
import ProcessData from "./components/process/ProcessData.vue";
import Budget from "./components/budget_management/Budget.vue";

export default {
  components: {
    Category,
    Transaction,
    ProcessData,
    MainDashboard,
    Budget
  },
  data() {
    return {
      tab_value: "home"
    };
  }
};
</script>

<style lang="sass" src="bulma"></style>


