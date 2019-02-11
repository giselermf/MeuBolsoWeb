<template>
  <div>
     <div class="field is-grouped is-grouped-right" style="padding-top: 10px;">
    <p class="control">
        <button class="button is-link" @click="onAdd()" >Add</button>
    </p>
    </div>
    <my-vuetable ref="vuetableTransaction"
        api-url="http://127.0.0.1:5000/transactionsFiltered/"
        :fields="fields"
        :sort-order="sortOrder"
        :append-params="appendParams"
    >
        <template slot="actions" scope="props">
            <a style="font-size: 13px; padding-right: 11px;cursor:pointer" @click="onEdit(props.rowData)">✏️</a>
            <a style="font-size: 13px; padding-right: 11px;cursor:pointer" @click="onSplit(props.rowData)">✂️️</a>
            <a style="font-size: 13px; padding-right: 11px;cursor:pointer" @click="onAddRecurrence(props.rowData)">+</a>
        </template>
    </my-vuetable>
    <transaction-edit v-if="showModal" @close="showModal = false" :action="action" :transaction="selected_transaction" ></transaction-edit>
  </div>
</template>

<script>
import MyVuetable from "../util/MyVuetable.vue";
import Vue from 'vue'
import VueEvents from 'vue-events';
import TransactionEdit from "./TransactionEditModal.vue";
Vue.use(VueEvents);

export default {
  components: {
    MyVuetable, TransactionEdit
  },
  props: ["params"],
  mounted() {
    this.$events.$on("transaction-filter-set", eventData => this.onFilterSet(eventData));
    this.$events.$on("close-transaction-split-modal", eventData =>
      this.onModalClose(eventData)
    );
  },
  data() {
    return {
      showModal: false,
      selected_transaction: "",
      action: null,
      fields: [
        {
          name: "account",
          title: "Bank Name",
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
          dataClass: "center aligned",
          callback: "formatFloat"
        },
        {
          name: "Date",
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
      appendParams: this.params
    };
  },
  methods: {
    onSplit(data) {
      this.showModal = true;
      this.action= "split";
      this.selected_transaction = data;
    },
    onAddRecurrence(data) {
      this.showModal = true;
      this.action= "add";
      this.selected_transaction = data;
    },
    onAdd() {
      this.showModal = true;
      this.action= "add";
      this.selected_transaction = {};
    },
    onModalClose(eventData) {
      this.showModal = false;
      this.action= null;
      if (this.$refs.vuetableTransaction)
        Vue.nextTick(() => this.$refs.vuetableTransaction.$refs.vuetable.refresh());
    },
    onEdit(data) {
      this.showModal = true;
      this.action= "edit";
      this.selected_transaction = data;
      this.$events.fire("edit-record", data);
    },
    onFilterSet(filterParams) {
      this.appendParams.filter = filterParams;
      if (this.$refs.vuetableTransaction)
        Vue.nextTick(() => this.$refs.vuetableTransaction.$refs.vuetable.refresh());
    }
  }
};
</script>


