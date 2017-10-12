<template>
  <div class="container">
    <tabs animation="slide" :only-fade="false">
      <tab-pane label="Home" selected>Home
        <dashboard></dashboard>
      </tab-pane>
      <tab-pane label="Categories">Categories
            <category></category>
      </tab-pane>
      <tab-pane label="Bank Records">Bank Records
        <transaction></transaction>
      </tab-pane>
      <tab-pane label="About">About</tab-pane>
    </tabs>
  </div>
</template>

<script>
  import { Tabs, TabPane } from 'vue-bulma-tabs'
  import Category from './components/data_management/Category.vue'
  import Transaction from './components/data_management/Transaction.vue'
  import Dashboard from './components/Dashboard.vue'

  export default {
    components: {
      Tabs,TabPane, Category, Dashboard, Transaction
    }
  }
</script>

<style lang="sass">
  @import '~bulma'
</style>