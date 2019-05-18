<template>
  <v-app>
    <v-toolbar app>
      <v-toolbar-title class="headline text-uppercase">
        <span class="font-weight-light">Meu Bolso</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
    <v-content>
      <div id="app">
        <v-app id="inspire">
          <div>
            <v-tabs centered color="cyan" dark icons-and-text>
              <v-tabs-slider color="yellow"></v-tabs-slider>

              <v-tab href="#tab-1">
                Dashboard
                <v-icon>dashboard</v-icon>
              </v-tab>

              <v-tab href="#tab-2">
                Transactions
                <v-icon>attach_money</v-icon>
              </v-tab>

              <v-tab href="#tab-3">
                Cateogories
                <v-icon>category</v-icon>
              </v-tab>

              <v-tab href="#tab-4">
                Investiments
                <v-icon>attach_money</v-icon>
              </v-tab>

              <v-tab href="#tab-5">
                Process Data
                <v-icon>add_circle_outline</v-icon>
              </v-tab>

              <v-tab-item :value="'tab-1'">
                <v-card flat>
                  <main-dashboard></main-dashboard>
                </v-card>
              </v-tab-item>

              <v-tab-item :value="'tab-2'">
                <v-card flat>
                  <transactions :showOverMonth="true" :accountTypes="['Checking Account', 'Credit Card']"></transactions>
                </v-card>
              </v-tab-item>

              <v-tab-item :value="'tab-3'">
                <v-card flat>
                  <category-table></category-table>
                </v-card>
              </v-tab-item>

              <v-tab-item :value="'tab-4'">
                <v-card flat>
                  <transactions :accountTypes="['Savings']" v-bind:dateFromDelta="-30"></transactions>
                </v-card>
              </v-tab-item>

              <v-tab-item :value="'tab-5'">
                <v-card flat>
                 <process-data></process-data>
                </v-card>
              </v-tab-item>

            </v-tabs>
          </div>
        </v-app>
      </div>
    </v-content>
  </v-app>
</template>

<script>
import Transactions from "./components/Transactions";
import CategoryTable from "./components/CategoryTable";
import ProcessData from "./process/ProcessData.vue";
import MainDashboard from "./components/MainDashboard.vue";

export default {
  name: "App",
  components: {
    Transactions,
    CategoryTable,ProcessData, MainDashboard
    
  },
  data() {
    return {
    };
  }
};
</script>
