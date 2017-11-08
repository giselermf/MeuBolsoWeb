<script>
import GenericFilter from './GenericFilter.vue'

export default {
  extends: GenericFilter,
  data() {
    return {
      url: 'http://127.0.0.1:5000/getDistinctSubCategories?',
      placeholder:"All SubCategories",
      label:"SubCategory",
      trackBy:"SubCategory",
      filterName: "filter_subcategories"
    }
  }
}
</script>
