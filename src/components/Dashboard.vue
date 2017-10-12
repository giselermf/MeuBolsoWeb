<template>
  <div>
    <canvas ref="canvas" width="0" height="0"></canvas>
    <div class="tile is-ancestor">
      <div class="tile is-parent">
        <article class="tile is-child box">
          <p class="title">Filter</p>
          <p class="subtitle">Bank</p>
        </article>
      </div>
      <div class="tile is-parent">
        <article class="tile is-child box">
          <p class="title">Filter</p>
          <p class="subtitle">Year</p>
        </article>
      </div>
      <div class="tile is-parent">
        <article class="tile is-child box">
          <p class="title">Filter</p>
          <p class="subtitle">Type</p>
        </article>
      </div>
    </div>

    <div class="tile is-ancestor">
        <div class="tile is-parent">
        <article class="tile is-child box">
          <p class="title">Filter</p>
          <p class="subtitle">Category</p>
        </article>
      </div>
      <div class="tile is-parent">
        <article class="tile is-child box">
          <p class="title">Filter</p>
          <p class="subtitle">Subcategory</p>
        </article>
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

export default {
  components: {
    LineExample, CategoryDoughnut
  },
}
</script>

<style lang="scss" scoped>
</style>