<template>
<div class="container">
    <div id="app" class="ui horizontal segments" >
      <div class="ui  segment">
          <transaction-search></transaction-search>
      </div>  
      <div class="ui  segment"> 
      <dashboard></dashboard> 
      </div> 
    </div>
        <transaction-table></transaction-table>

</div>
</template>

<script>
  import TransactionSearch from './TransactionSearch.vue'
  import Dashboard from './TransactionDashboard.vue'
  import TransactionTable from './TransactionTable.vue'

  export default {
    components: {
      TransactionSearch,TransactionTable,Dashboard
    }
  }
</script>s