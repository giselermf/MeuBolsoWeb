

<template>
   <transition name="modal">
  <div class="modal modal-mask ">
  <div class="modal-background"></div>
  <div class="modal-card">
    <header class="modal-card-head">
      <p class="modal-card-title">Select Category</p>
    </header>
    <section class="modal-card-body">
        <div>
            <label class="label">Type:</label>
            <select class="select" v-model="selectedType" v-on:change="onChangeType" >
                <option v-for="type in getTypes()" v-bind:key="type" v-bind:value="type">
                    {{ type }}
                </option>
            </select>
        </div>
        <div>
            <label class="label">Category:</label>
            <select class="select" v-model="selectedCategory" v-on:change="onChangeCategory">
                <option v-for="category in getCategories()" v-bind:key="category" v-bind:value="category">
                    {{ category }}
                </option>
            </select>
        </div>
        <div>
            <label class="label">SubCategory:</label>
            <select class="select" v-model="selectedSubCategory">
                <option v-for="subcategory in getSubCategories()" v-bind:key="subcategory" v-bind:value="subcategory">
                    {{ subcategory }}
                </option>
            </select>
        </div> 
    </section>
    <footer class="modal-card-foot">
      <button class="button is-success" @click="CloseModal">Close</button>
    </footer>
  </div>
</div>
</transition>
</template>

<script>
import CategorySelectCombos from "../util/CategorySelectCombos.vue"

export default {
  mixins : [CategorySelectCombos],
  methods: {
      CloseModal() {
          let data = {
              selectedType : this.selectedType,
              selectedCategory : this.selectedCategory,
              selectedSubCategory : this.selectedSubCategory,
              categoryId: this.getSelectedCategoryId()
          }
          
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
  background-color: rgba(0, 0, 0, .5);
  display: table;
  transition: opacity .3s ease;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
}

.modal-container {
  width: 500px;
  height: 220px;
  margin: 0px auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, .33);
  transition: all .3s ease;
  font-family: Helvetica, Arial, sans-serif;
}

.modal-default-button {
  float: right;
}

</style>
