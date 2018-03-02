<template>
<div class="container">
    <transaction-search></transaction-search>
    <transaction-table></transaction-table>
</div>
</template>

<script>
  //import TransactionEdit from './TransactionEdit.vue'
  import TransactionSearch from './TransactionSearch.vue'
  import TransactionTable from './TransactionTable.vue'

  export default {
    components: {
      TransactionSearch,TransactionTable
    }
  }
</script>s