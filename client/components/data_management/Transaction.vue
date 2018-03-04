<template>
<div class="container">
    <transaction-search></transaction-search>
    <dashboard></dashboard>
    <transaction-table></transaction-table>
</div>
</template>

<script>
  import TransactionSearch from './TransactionSearch.vue'
  import Dashboard from './Dashboard.vue'
  import TransactionTable from './TransactionTable.vue'

  export default {
    components: {
      TransactionSearch,TransactionTable,Dashboard
    }
  }
</script>s