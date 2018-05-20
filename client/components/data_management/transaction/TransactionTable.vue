<template>
  <div>
    <my-vuetable ref="vuetableTransaction"
        api-url="http://127.0.0.1:5000/transactionsFiltered/"
        :fields="fields"
        :sort-order="sortOrder"
        :append-params="appendParams"
    >
        <template slot="actions" scope="props">
            <a style="font-size: 20px; padding-right: 11px;cursor:pointer" @click="onSplit(false, props.rowData)">✏️</a>
            <a style="font-size: 20px; padding-right: 11px;cursor:pointer" @click="onSplit(true, props.rowData)">✂️️</a>
        </template>
    </my-vuetable>
    <transaction-edit v-if="showModal" @close="showModal = false" :split="split" :selectedTransaction="selected_transaction" ></transaction-edit>
  </div>
</template>

<script>
import MyVuetable from "../MyVuetable";
import Vue from 'vue'
import VueEvents from 'vue-events';
import TransactionEdit from "./TransactionEditModal.vue";
Vue.use(VueEvents);

export default {
  components: {
    MyVuetable, TransactionEdit
  },
  mounted() {
    this.$events.$on("transaction-filter-set", eventData => this.onFilterSet(eventData));
    this.$events.$on("transaction-filter-reset", e => this.onFilterReset());
    this.$events.$on("close-transaction-split-modal", eventData =>
      this.onModalClose(eventData)
    );
  },
  data() {
    return {
      showModal: false,
      split: false,
      selected_transaction: "",
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
        {
          name: "Currency",
          titleClass: "center aligned",
          dataClass: "center aligned"
        },
        {
          name: "AmountEUR",
          title: "Amount (EUR)",
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
    onSplit(split, data) {
      this.showModal = true;
      this.split = split
      this.selected_transaction = data;
    },
    onModalClose(eventData) {
      this.showModal = false;
      this.split = false;
      this.onFilterSet();
    },
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


