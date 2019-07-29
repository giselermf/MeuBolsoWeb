<template>
  <v-layout row wrap>
    <v-flex xs12 sm6 md4>
      <v-menu
        :close-on-content-click="false"
        :nudge-right="40"
        transition="scale-transition"
        offset-y
        full-width
        min-width="290px"
      >
        <template v-slot:activator="{ on }">
          <v-text-field
            v-model="dateFrom"
            label="Date From"
            prepend-icon="event"
            readonly
            v-on="on"
          ></v-text-field>
        </template>
        <v-date-picker v-model="dateFrom" @input="menuDF = false"></v-date-picker>
      </v-menu>
    </v-flex>

    <v-flex xs12 sm6 md4>
      <v-menu
        :close-on-content-click="false"
        :nudge-right="40"
        transition="scale-transition"
        offset-y
        full-width
        min-width="290px"
      >
        <template v-slot:activator="{ on }">
          <v-text-field v-model="dateTo" label="Date To" prepend-icon="event" readonly v-on="on"></v-text-field>
        </template>
        <v-date-picker v-model="dateTo" @input="menuDT = false"></v-date-picker>
      </v-menu>
    </v-flex>
  </v-layout>
</template>

<script>
import moment from "moment";
export default {
  props: {
    dateFromDelta: {
      type: Number,
      default: -1
    },
    dateToDelta: {
      type: Number,
      default: 1
    }
  },
  name: "date_range",
  data: () => ({
    dateFrom: null,
    dateTo: null
  }),
  computed: {
    fromAndTo() {
      return `${this.dateFrom}|${this.dateTo}`;
    },
  },
  mounted() {
    this.dateFrom = moment(new Date())
      .add(this.dateFromDelta, "month")
      .startOf("month")
      .format("YYYY-MM-DD");
    this.dateTo = moment(new Date())
      .add(this.dateToDelta, "month")
      .endOf("month")
      .format("YYYY-MM-DD");
  },
  watch: {
    fromAndTo: function(newVal, oldVal) {
      if (newVal != oldVal) this.$emit("date_range_updated");
    },
  },
  methods: {
    getFromDate() {
      return this.dateFrom;
    },
    getToDate() {
      return this.dateTo;
    }
  }
};
</script>