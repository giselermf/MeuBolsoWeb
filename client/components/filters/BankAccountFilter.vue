<script>
import GenericFilter from './GenericFilter.vue'

export default {
  extends: GenericFilter,
  data() {
    return {
      url: 'http://127.0.0.1:5000/getDistinctBankAccounts?',
      placeholder:"All Bank Accounts",
      label:"BankName",
      trackBy:"BankName",
      filterName: "filter_bankAccounts"
    }
  }
}

</script>