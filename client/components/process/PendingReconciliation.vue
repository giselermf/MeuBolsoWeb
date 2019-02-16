<template>
    <tr>
        <td>
            <div class="field is-horizontal-left" >
                <div class="field is-grouped">
                    <div class="control">
                        <input type="checkbox" id="keep2" value="keep2" v-model="keep2">
                    </div>
                    <div class="field is-vertical-left">
                        {{row.transaction2.TransactionNumber}}
                        <p></p>
                        {{row.transaction2.Description}}
                        <p></p>
                        {{row.transaction2.AmountEUR}}
                        <p></p>
                        {{row.transaction2.Date}}
                        <p></p>
                        {{row.transaction2.Type}} - {{row.transaction2.Category}} - {{row.transaction2.SubCategory}}
                    </div>
                </div>
            </div>
        </td>
        <td>
            <div class="field is-horizontal-left" >
                <div class="field is-grouped">
                    <div class="control">
                        <input type="checkbox" id="keep1" value="keep1" v-model="keep1">
                    </div>
                    <div class="field is-vertical-left">
                        {{row.transaction1.TransactionNumber}}
                        <p></p>
                        {{row.transaction1.Description}}
                        <p></p>
                        {{row.transaction1.AmountEUR}}
                        <p></p>
                        {{row.transaction1.Date}}
                        <p></p>
                        {{row.transaction1.Type}} - {{row.transaction1.Category}} - {{row.transaction1.SubCategory}}
                    </div>
                </div>
            </div>
        </td>
        <td>
            <div>
                <button class="button is-link" @click="onProcess()">Process</button>
            </div>
        </td>
    </tr>
</template>

<script>
import {HTTP} from '../util/http-common';

export default {
    props: ["row"],
    data: function () {
            return {
                keep1: false,
                keep2: false
            }
        },
    methods: {
        onProcess() {
            HTTP.post(
                "ProcessReconciliation/",
                querystring.stringify({
                    reconciliation_id: this.row.id,
                    transaction1_id: this.row.transaction1.id,
                    transaction1_keep: this.keep1,
                    transaction2_id: this.row.transaction2.id,
                    transaction2_keep: this.keep2})
                )
                .then(response => {
                    this.$events.fire("reconcilitions-refresh", response);
                })
                .catch(function(error) {
                    console.log(error);
                });
        }
    }
};
</script>