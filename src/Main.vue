<template>
  <div class="container">
    <tabs animation="slide" :only-fade="false">
      <tab-pane label="Home">Home</tab-pane>
      <tab-pane label="Categories" selected>Categories
            <category></category>
      </tab-pane>
      <tab-pane label="About">About</tab-pane>
    </tabs>
  </div>
</template>

<script>
  import { Tabs, TabPane } from 'vue-bulma-tabs'
  import Category from './components/Category/Category.vue'

  export default {
    components: {
      Tabs,TabPane, Category
    }
  }
</script>

<style lang="sass">
  @import '~bulma'
</style>