<template>
  <div>
    <canvas ref="canvas" width="0" height="0"></canvas>
    <div class="tile is-ancestor">
      <div class="tile is-vertical is-6">
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
      <div class="tile is-vertical is-6">
          <div class="tile is-parent">
            <article class="tile is-child box">
              <div class="Chart">
                <h2>Amount by Category</h2>
                <meu-bolso-pie url="http://127.0.0.1:5000/getAmountBySubCategory?" label="SubCategory" ></meu-bolso-pie>
              </div>
            </article>
        </div>
      </div>
      <div class="tile is-vertical is-6">
          <div class="tile is-parent">
            <article class="tile is-child box">
              <div class="Chart">
                <h2>Amount by Category/Month</h2>
                <meu-bolso-bar url="http://127.0.0.1:5000/getAmountByYearMonthAndSubCategory?" xLabel="yearmonth" datasetLabel="SubCategory"></meu-bolso-bar>
              </div>
            </article>
        </div>
      </div>
    </div>
    <div class="tile is-ancestor">
      <div class="tile is-vertical is-12">
          <div class="Chart">
            <h2>Running Balance</h2>
            <meu-bolso-line url="http://127.0.0.1:5000/getRunningBalance?" xLabel="Date" datasetLabel="BankName" ></meu-bolso-line>
          </div>
      </div> 
    </div>
  </div>
</template>

<script>
import meuBolsoPie from './charts/MeuBolsoPie.js'
import meuBolsoBar from './charts/MeuBolsoBar.js'
import meuBolsoLine from './charts/MeuBolsoLine.js'
import YearFilter from './filters/YearFilter.vue'
import CategoryFilter from './filters/CategoryFilter.vue'
import TypeFilter from './filters/TypeFilter.vue'
import SubcategoryFilter from './filters/SubcategoryFilter.vue'

export default {
  components: {
    YearFilter, CategoryFilter, TypeFilter, SubcategoryFilter, meuBolsoPie, meuBolsoBar, meuBolsoLine
  },

}
</script>

<style lang="scss" scoped>
</style>