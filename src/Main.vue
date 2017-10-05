<template>
  <div class="container">
    <tabs animation="slide" :only-fade="false">
      <tab-pane label="Home" selected>Home
         <my-chart></my-chart>

      </tab-pane>
      <tab-pane label="Categories">Categories
            <category></category>
      </tab-pane>
      <tab-pane label="Bank Records">Bank Records
      </tab-pane>
      <tab-pane label="About">About</tab-pane>
    </tabs>
  </div>
</template>

<script>
  import { Tabs, TabPane } from 'vue-bulma-tabs'
  import Category from './components/Category/Category.vue'
  import MyChart from './components/MyChart.vue'

  export default {
    components: {
      Tabs,TabPane, Category, MyChart
    }
  }
</script>

<style lang="sass">
  @import '~bulma'
</style>