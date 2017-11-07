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
                <h2>Amount by Category</h2>
                <meu-bolso-pie url="http://127.0.0.1:5000/getAmountBySubCategory?" label="SubCategory" ></meu-bolso-pie>
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
                <meu-bolso-bar url="http://127.0.0.1:5000/getAmountByYearMonthAndSubCategory?" label="SubCategory" ></meu-bolso-bar>
              </div>
            </article>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import meuBolsoPie from './charts/MeuBolsoPie.js'
import meuBolsoBar from './charts/MeuBolsoBar.js'
import YearFilter from './filters/YearFilter.vue'
import CategoryFilter from './filters/CategoryFilter.vue'
import TypeFilter from './filters/TypeFilter.vue'
import SubcategoryFilter from './filters/SubcategoryFilter.vue'

export default {
  components: {
    YearFilter, CategoryFilter, TypeFilter, SubcategoryFilter, meuBolsoPie, meuBolsoBar
  },

}
</script>

<style lang="scss" scoped>
</style>