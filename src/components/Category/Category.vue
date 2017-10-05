<template>
<div class="container">
    <category-edit></category-edit>
    <category-table></category-table>
</div>
</template>

<script>
  import CategoryEdit from './CategoryEdit.vue'
  import CategoryTable from './CategoryTable.vue'

  export default {
    components: {
      CategoryEdit,CategoryTable
    }
  }
</script>s