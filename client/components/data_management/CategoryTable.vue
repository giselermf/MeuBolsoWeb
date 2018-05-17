<template>
  <div >
    <my-vuetable ref="vuetableCategory"
          api-url="http://127.0.0.1:5000/categories/"
          :fields="fields"
          :sort-order="sortOrder"
          :append-params="appendParams"
        >
            <template slot="actions" scope="props">
                <a style="font-size: 20px; padding-right: 11px;cursor:pointer" @click="onEdit(props.rowData)">&#10000;</a>
                <a style="cursor:pointer" @click="onDelete(props.rowData)"> &#10060;</a>
            </template>
        </my-vuetable>
  </div>
</template>


<script>
import MyVuetable from ".//MyVuetable";
import VueEvents from 'vue-events';
import Vue from 'vue'
Vue.use(VueEvents);

export default {
  props: ["filters"],
  components: {
    MyVuetable
  },
  watch: {
    filters: function(val) {
      this.fullName = val + " " + this.lastName;
    }
  },
  mounted() {
    this.$events.$on("category-filter-set", eventData =>
      this.onFilterSet(eventData)
    );
    this.$events.$on("category-filter-reset", e => this.onFilterReset());
  },
  data() {
    return {
      selected_id: "",
      selected_category: "",
      selected_description: "",
      fields: [
        {
          name: "Type",
          titleClass: "center aligned",
          dataClass: "center aligned"
        },
        {
          name: "Category",
          titleClass: "center aligned",
          dataClass: "center aligned"
        },
        {
          name: "SubCategory",
          titleClass: "center aligned",
          dataClass: "center aligned"
        },
        {
          name: "Description",
          titleClass: "center aligned",
          dataClass: "center aligned",
          callback: "formatDescription"
        },
        {
          name: "__slot:actions",
          title: "Actions",
          titleClass: "center aligned",
          dataClass: "center aligned"
        }
      ],
      sortOrder: [
        {
          field: "category",
          sortField: "category",
          direction: "asc"
        }
      ],
      appendParams: {}
    };
  },
  methods: {
    onEdit(data) {
      this.$events.fire("edit-record", data);
      this.selected_id = data.id;
      this.selected_category = data.Category;
      this.selected_description = data.Description;
    },
    onDelete(data) {
      this.$events.fire("delete-record", data);
      this.selected_id = data.id;
      this.selected_category = data.Category;
      this.selected_description = data.Description;
    },
    onFilterSet(filterParams) {
      this.appendParams.filter = filterParams;
      Vue.nextTick(() => this.$refs.vuetableCategory.$refs.vuetable.refresh());
    },
    onFilterReset() {
      delete this.appendParams.filter;
      Vue.nextTick(() => this.$refs.vuetableCategory.$refs.vuetable.refresh());
    }
  }
};
</script>




