<template>
    <tr>
        <table-cell
            v-for="val in columns" :key="val"
            :isHeader="isHeader(val)"
            :element="row[val]"
        ></table-cell>

    </tr>
</template>

<script>
import TableCell from "./TableCell.vue";
export default {
  props: ["row", "columns", "firstColumnLabel"],
  components: {
    TableCell
  },
    methods: {
      isHeader(index) {
          return index == this.firstColumnLabel;
      }

  }
};
</script>