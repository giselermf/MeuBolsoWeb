<template>
    <tr>
        <budget-cell
            v-for="val in columns" :key="val.Name"
            :isHeader = val.isHeader
            :Month = val.Month
            :Year = val.Year
            :element="getElement(val.isHeader, val.Name, val.Month, val.Year)"
            :categoryId="row.category_id"      
        ></budget-cell>

    </tr>
</template>

<script>
import BudgetCell from "./BudgetCell.vue";
export default {
  props: ["row", "columns"],
  components: {
    BudgetCell
  },
  methods: {
    getElement(isHeader, Name, Month, Year) {
      if (!isHeader) {
        for (let e in this.row) {
          if (this.row[e].Month == Month && this.row[e].Year == Year) {
            return this.row[e];
          }
        }
      } else {
        return this.row[Name];
      }
    }
  }
};
</script>