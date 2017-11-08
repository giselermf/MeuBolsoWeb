<script>
import GenericFilter from './GenericFilter.vue'

export default {
  extends: GenericFilter,
  data() {
    return {
      url: 'http://127.0.0.1:5000/getDistinctTypes?',
      placeholder:"All types",
      label:"Type",
      trackBy:"Type",
      filterName: "filter_type"
    }
  }
}
</script>
