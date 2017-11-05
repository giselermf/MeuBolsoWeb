<template>
  <div>
    <canvas ref="canvas" width="0" height="0"></canvas>
    <div class="tile is-ancestor">
      <div class="tile is-vertical is-12">
          <div class="tile is-parent">
            <article class="tile is-child box">
              <year-filter></year-filter>
              <type-filter></type-filter>
              <category-filter></category-filter>
              <subcategory-filter></subcategory-filter>
        </article>
      </div>
    </div>
    </div>

    <div class="tile is-ancestor">
      <div class="tile is-vertical is-12">
          <div class="tile is-parent">
            <article class="tile is-child box">
              <div class="Chart">
                <h2>Linechart</h2>
                <line-example></line-example>
              </div>
            </article>
        </div>
      </div>
    </div>
    <div class="tile is-ancestor">
      <div class="tile is-vertical is-12">
          <div class="tile is-parent">
            <article class="tile is-child box">
              <div class="Chart">
                <h2>Amount by Category</h2>
                <category-doughnut></category-doughnut>
              </div>
            </article>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import LineExample from './LineChart.js'
import CategoryDoughnut from './charts/CategoryDoughnut.js'
import YearFilter from './filters/YearFilter.vue'
import CategoryFilter from './filters/CategoryFilter.vue'
import TypeFilter from './filters/TypeFilter.vue'
import SubcategoryFilter from './filters/SubcategoryFilter.vue'

export default {
  components: {
    LineExample, CategoryDoughnut, YearFilter, CategoryFilter, TypeFilter, SubcategoryFilter
  },

}
</script>

<style lang="scss" scoped>
</style>