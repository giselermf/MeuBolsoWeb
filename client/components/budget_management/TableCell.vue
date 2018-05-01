<template>
    <td>{{value}}</td>
</template>

<script>
export default {
  props: ["element", "isHeader"],
  components: {},
  data() {
    return { value: this.getData() };
  },
  methods: {
    getData() {
      console.log("isHeader", this.isHeader);
      if (this.element != undefined) {
        if (this.isHeader) return this.element;
        return this.element.Actuals + "/" + this.element.Budget;
      }
    }
  }
};
</script>