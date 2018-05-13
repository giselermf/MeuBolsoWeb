

<template>
   <transition name="modal">
  <div class="modal modal-mask ">
  <div class="modal-background"></div>
  <div class="modal-card">
    <header class="modal-card-head">
      <p class="modal-card-title">Select Category</p>
    </header>
    <section class="modal-card-body">
        <category-select-combos ref="typecombos" ></category-select-combos>
    </section>
    <footer class="modal-card-foot">
      <button class="button is-success" @click="CloseModal">Close</button>
    </footer>
  </div>
</div>
</transition>
</template>

<script>
import CategorySelectCombos from "../util/CategorySelectCombos.vue";

export default {
  components: {
    CategorySelectCombos
  },
  methods: {
    CloseModal() {
      let data = {
        selectedType: this.$refs.typecombos.getSelectedType(),
        selectedCategory: this.$refs.typecombos.getSelectedCategory(),
        selectedSubCategory: this.$refs.typecombos.getSelectedSubCategory(),
        categoryId: this.$refs.typecombos.getSelectedCategoryId()
      };
      this.$events.fire("close-category-modal", data);
    }
  }
};
</script>

<style>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: table;
  transition: opacity 0.3s ease;
}

.modal-container {
  width: 500px;
  height: 220px;
  margin: 0px auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;
  font-family: Helvetica, Arial, sans-serif;
}

.modal-default-button {
  float: right;
}
</style>
