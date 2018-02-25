<template>
<div class="container">
    <transaction-edit></transaction-edit>
    <transaction-table></transaction-table>
</div>
</template>

<script>
  import TransactionEdit from './TransactionEdit.vue'
  import TransactionTable from './TransactionTable.vue'

  export default {
    components: {
      TransactionEdit,TransactionTable
    }
  }
</script>s