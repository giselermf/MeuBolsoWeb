<template>
    <div>
        <my-vuetable ref="vuetableTransaction"
                api-url="http://127.0.0.1:5000/transactionsFiltered/"
                :fields="fields"
                :sort-order="sortOrder"
                :append-params="appendParams"
            >
                <template slot="actions" scope="props">
                    <a style="font-size: 20px; padding-right: 11px;cursor:pointer" @click="onEdit(props.rowData)">&#10000;</a>
                </template>
            </my-vuetable>
    </div>
</template>

<script>
import MyVuetable from ".//MyVuetable";
import Vue from 'vue'
import VueEvents from 'vue-events';
Vue.use(VueEvents);

export default {
  components: {
    MyVuetable
  },
  mounted() {
    this.$events.$on("transaction-filter-set", eventData => this.onFilterSet(eventData));
    this.$events.$on("transaction-filter-reset", e => this.onFilterReset());
  },
  data() {
    return {
      selected_id: "",
      selected_category: "",
      selected_description: "",
      fields: [
        {
          name: "BankName",
          titleClass: "center aligned",
          dataClass: "center aligned"
        },
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
          dataClass: "center aligned"
        },
        /*   {
                        name: 'TransactionNumber',
                        titleClass: 'center aligned',
                        dataClass: 'center aligned',
                    },*/
        {
          name: "Currency",
          titleClass: "center aligned",
          dataClass: "center aligned"
        },
        {
          name: "Amount",
          titleClass: "center aligned",
          dataClass: "center aligned"
        },
        {
          name: "Date_str",
          titleClass: "center aligned",
          dataClass: "center aligned"
        },
        {
          name: "__slot:actions",
          title: "Slot Actions",
          titleClass: "center aligned",
          dataClass: "center aligned"
        }
      ],
      sortOrder: [
        {
          field: "Date",
          sortField: "Date",
          direction: "desc"
        }
      ],
      appendParams: {}
    };
  },
  methods: {
    onEdit(data) {
      this.$events.fire("edit-record", data);
    },
    onFilterSet(filterParams) {
      this.appendParams.filter = filterParams;
      Vue.nextTick(() => this.$refs.vuetableTransaction.$refs.vuetable.refresh());
    },
    onFilterReset() {
      delete this.appendParams.filter;
      Vue.nextTick(() => this.$refs.vuetableTransaction.$refs.vuetable.refresh());
    }
  }
};
</script>

<style>
.ui.table td {
  padding: 1px;
}
</style>


