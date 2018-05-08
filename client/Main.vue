<template>
  <div class="container">
    <tabs animation="slide" :only-fade="false">
      <tab-pane label="Bank Records">
        <main-dashboard></main-dashboard>
      </tab-pane>
      <tab-pane label="Bank Records">
        <transaction></transaction>
      </tab-pane>
      <tab-pane label="Categories">
            <category></category>
      </tab-pane>
      <tab-pane label="Budget">
        <budget></budget>
      </tab-pane>
      <tab-pane label="Process Records">
        <process-data></process-data>
      </tab-pane>
      <tab-pane label="About">About</tab-pane>
    </tabs>
  </div>
</template>

<script>
import { Tabs, TabPane } from "vue-bulma-tabs";
import MainDashboard from "./components/main_dashboard/MainDashboard.vue";
import Category from "./components/data_management/CategoryEdit.vue";
import Transaction from "./components/data_management/Transaction.vue";
import ProcessData from "./components/process/ProcessData.vue";
import Budget from "./components/budget_management/Budget.vue";

export default {
  components: {
    Tabs,
    TabPane,
    Category,
    Transaction,
    ProcessData,
    MainDashboard,
    Budget
  }
};
</script>



<style lang="sass">
    @import '~bulma'
</style>
