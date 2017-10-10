<template>
  <div>
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
      <div class="tile is-parent is-6">
        <article class="tile is-child box">
          <h4 class="title">Amount in Euro by Category</h4>
          <div class="content">
            <chart :type="'doughnut'" :data="chartData"></chart>
          </div>
        </article>
      </div>
    </div>

    <div class="tile is-ancestor">
      <div class="tile is-vertical is-12">
          <div class="tile is-parent">
            <article class="tile is-child box">
              <p class="title">Expense by Category/Month</p>
              <div class="content">
                <chart :type="'bar'" :data="chartData"></chart>
              </div>
            </article>
        </div>
      </div>
    </div>
    <div class="tile is-ancestor">
      <div class="tile is-vertical is-12">
          <div class="tile is-parent">
            <article class="tile is-child box">
              <p class="title">Data</p>
              <div class="content">
                <p> Transactioin list </p>
              </div>
            </article>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from 'vue-bulma-chartjs'
export default {
  components: {
    Chart
  },
  data () {
    return {
      data: [300, 50, 100]
    }
  },
  computed: {
    chartData () {
      return {
        labels: [
          'Red',
          'Blue',
          'Yellow'
        ],
        datasets: [{
          data: this.data,
          backgroundColor: [
            '#FF6384',
            '#36A2EB',
            '#FFCE56'
          ]
        }]
      }
    }
  },
  mounted () {
    setInterval(() => {
      // https://github.com/vuejs/vue/issues/2873
      // Array.prototype.$set/$remove deprecated (use Vue.set or Array.prototype.splice instead)
      this.data.forEach((item, i) => {
        this.data.splice(i, 1, Math.ceil(Math.random() * 1000))
      })
    }, 1024)
  }
}
</script>

<style lang="scss" scoped>
</style>