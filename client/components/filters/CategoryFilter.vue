<script>
import GenericFilter from './GenericFilter.vue'

export default {
  extends: GenericFilter,
  data() {
    return {
      url: 'http://127.0.0.1:5000/getDistinctCategories?',
      placeholder:"All Categories",
      label:"Category",
      trackBy:"Category",
      filterName: "filter_categories"
    }
  }
}
</script>