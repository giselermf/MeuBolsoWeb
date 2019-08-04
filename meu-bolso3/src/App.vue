<template>
  <v-app>
    <v-card
    color="grey lighten-4"
    flat
    height="200px"
    tile
  >
    <v-toolbar color="primary"
      extended extension-height="80">
      <v-toolbar-title>Meu Bolso</v-toolbar-title>

      <v-spacer></v-spacer>

      <template v-slot:extension >
        <v-tabs centered icons-and-text v-model="model">
          <v-tabs-slider ></v-tabs-slider>

          <v-tab href="#tab-1" :key="1">
            Dashboard
            <v-icon>dashboard</v-icon>
          </v-tab>

          <v-tab href="#tab-2" :key="2">
            Transactions
            <v-icon>attach_money</v-icon>
          </v-tab>

          <v-tab href="#tab-3" :key="3">
            Cateogories
            <v-icon>category</v-icon>
          </v-tab>

          <v-tab href="#tab-4" :key="4">
            Investiments
            <v-icon>attach_money</v-icon>
          </v-tab>

          <v-tab href="#tab-5" :key="5">
            How much do I have?
            <v-icon>attach_money</v-icon>
          </v-tab>

          <v-tab href="#tab-6" :key="6">
            Process Data
            <v-icon>add_circle_outline</v-icon>
          </v-tab>
        </v-tabs>
      </template>
    </v-toolbar>
    <v-tabs-items v-model="model">
      <v-tab-item :value="'tab-1'">
        <v-card flat class="padding-card">
          <main-dashboard></main-dashboard>
        </v-card>
      </v-tab-item>

      <v-tab-item :value="'tab-2'">
        <v-card flat class="padding-card">
          <transactions :showOverMonth="true" :accountTypes="['Checking Account', 'Credit Card']"></transactions>
        </v-card>
      </v-tab-item>

      <v-tab-item :value="'tab-3'">
        <v-card flat class="padding-card">
          <category-table></category-table>
        </v-card>
      </v-tab-item>

      <v-tab-item :value="'tab-4'">
        <v-card flat class="padding-card">
          <transactions :accountTypes="['Savings']" v-bind:dateFromDelta="-30"></transactions>
        </v-card>
      </v-tab-item>

      <v-tab-item :value="'tab-5'">
        <v-card flat class="padding-card">
          <overall-analysis :accountTypes="['Savings']" v-bind:dateFromDelta="-30"></overall-analysis>
        </v-card>
      </v-tab-item>

      <v-tab-item :value="'tab-6'">
        <v-card flat class="padding-card">
          <process-data></process-data>
        </v-card>
      </v-tab-item>
    </v-tabs-items>
    </v-card>
  </v-app>
</template>

<script>
import Transactions from "./components/Transactions";
import CategoryTable from "./components/CategoryTable";
import ProcessData from "./process/ProcessData.vue";
import MainDashboard from "./components/MainDashboard.vue";
import OverallAnalysis from "./components/OverallAnalysis.vue";

export default {
  name: "App",
  components: {
    Transactions,
    CategoryTable,
    ProcessData,
    MainDashboard,
    OverallAnalysis
  },
  data() {
    return {model:null};
  }
};
</script>

<style>
.padding-card {
  padding-top: 50px;
  padding-right: 30px;
  padding-bottom: 50px;
  padding-left: 80px;
}
</style>

