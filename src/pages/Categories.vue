<template>
  <main-layout>
    <h1>Categories</h1>
    <category-edit></category-edit>
    <category-table></category-table>
  </main-layout>
</template>

<script>
  import axios from 'axios';
  import MainLayout from '../layouts/Main'
  import CategoryEdit from '../components/Category/CategoryEdit'
  import CategoryTable from '../components/Category/CategoryTable'

  export default {
    components: {
      MainLayout,CategoryEdit, CategoryTable
    },
  }
</script>


