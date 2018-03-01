<template>
  <div class="container">
    <tabs animation="slide" :only-fade="false">
      <tab-pane label="Home" selected>
        <dashboard></dashboard>
      </tab-pane>
      <tab-pane label="Categories">
            <category></category>
      </tab-pane>
      <tab-pane label="Bank Records">
        <transaction></transaction>
      </tab-pane>
      <tab-pane label="Bank Records Search">
        <transaction-search></transaction-search>
      </tab-pane>
      <tab-pane label="Process Records">
        <process-data></process-data>
      </tab-pane>
      <tab-pane label="About">About</tab-pane>
    </tabs>
  </div>
</template>

<script>
  import { Tabs, TabPane } from 'vue-bulma-tabs'
  import Category from './components/data_management/Category.vue'
  import Transaction from './components/data_management/Transaction.vue'
  import TransactionSearch from './components/data_management/TransactionSearch.vue'
  import Dashboard from './components/Dashboard.vue'
  import ProcessData from './components/process/ProcessData.vue'

  export default {
    components: {
      Tabs,TabPane, Category, Dashboard, Transaction, ProcessData, TransactionSearch
    }
  }
</script>

<style lang="sass">
  @import '~bulma'
</style>