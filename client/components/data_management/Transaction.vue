<template>
<div class="container">
    <div id="app" class="ui horizontal segments" >
      <div class="ui  segment">
          <transaction-search></transaction-search>
      </div>  
      <div class="ui  segment">
        <transaction-table></transaction-table>
      </div>  
    </div>
  </div>
</template>

<script>
  import TransactionSearch from './TransactionSearch.vue'
  import TransactionTable from './TransactionTable.vue'

  export default {
    components: {
      TransactionSearch,TransactionTable
    }
  }
</script>s