<template>
    <div class="field is-horizontal-left" >
        <div class="field-body">
            <div class="field is-grouped">
                <p class="control">
                    <datepicker :typeable="true" v-model="fromDate" placeholder="from" :minimumView="minimumView" :maximumView="minimumView"></datepicker>
                </p>
                <p class="control">
                    <datepicker :typeable="true" v-model="toDate" placeholder="to" :minimumView="minimumView" :maximumView="minimumView"></datepicker>
                </p>
            </div>
        </div>    
    </div>
</template>

<script>
import moment from "moment";
import Datepicker from "vuejs-datepicker";

export default {
  props: ["minimumView"],
  components: {
    Datepicker
  },
  data() {
    return {
      toDate: null,
      fromDate: null
    };
  },
  methods: {
    getDateParams() {
      let params = {};
      if (this.fromDate) params["fromDate"] = moment(this.fromDate).format("YYYY-MM-DD");
      if (this.toDate) params["toDate"] = moment(this.toDate).format("YYYY-MM-DD");
      return JSON.stringify(params);
    },
    setRange(fromDelta, toDelta) {
      this.fromDate = moment(new Date())
        .add(fromDelta, this.minimumView)
        .startOf("month")
        .format("YYYY-MM-DD");
      this.toDate = moment(new Date())
        .add(toDelta, this.minimumView)
        .endOf("month")
        .format("YYYY-MM-DD");
    },
    resetValues() {
      this.fromDate = null;
      this.toDate = null;
    }
  }
};
</script>