<script>
import GenericFilter from './GenericFilter.vue'

export default {
  extends: GenericFilter,
  data() {
    return {
      options: [2017],
      url: 'http://127.0.0.1:5000/getDistinctYears?',
      placeholder:"All years",
      label:"Year",
      trackBy:"Year",
      filterName: "filter_year"
    }
  }
}

</script>