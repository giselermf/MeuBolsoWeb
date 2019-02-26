<template>
    <tr>
        <td>
            <div class="field is-horizontal-left" >
                <div class="field is-grouped">
                    <div class="field is-vertical-left">
                        Bank: {{row.transaction2.BankName}}
                        <p></p>
                        Number: {{row.transaction2.TransactionNumber}}
                        <p></p>
                        Desc: {{row.transaction2.Description}}
                        <p></p>
                        Amount: {{row.transaction2.Amount}}
                        <p></p>
                        Date: {{row.transaction2.Date}}
                        <p></p>
                        Catgory: {{row.transaction2.Type}} - {{row.transaction2.Category}} - {{row.transaction2.SubCategory}}
                    </div>
                </div>
            </div>
        </td>
        <td>
            <div class="field is-horizontal-left" >
                <div class="field is-grouped">
                    <div class="field is-vertical-left">
                        Bank: {{row.transaction1.BankName}}
                        <p></p>
                        Number: {{row.transaction1.TransactionNumber}}
                        <p></p>
                        Desc: {{row.transaction1.Description}}
                        <p></p>
                        Amount: {{row.transaction1.Amount}}
                        <p></p>
                        Date: {{row.transaction1.Date}}
                        <p></p>
                        Catgory: {{row.transaction1.Type}} - {{row.transaction1.Category}} - {{row.transaction1.SubCategory}}
                    </div>
                </div>
            </div>
        </td>
        <td>
            <div class="field is-vertical-left">
                <a class="field is-horizontal" v-on:click="onProcess(true, false)">Keep old</a>
                <p></p>
                <a class="field is-horizontal" v-on:click="onProcess(false, true)">Keep new</a>
                <p></p>
                <a class="field is-horizontal" v-on:click="onProcess(true, true)">Keep both</a>
            </div>
        </td>
    </tr>
</template>

<script>
import {HTTP} from '../util/http-common';
import querystring  from "querystring"

export default {
    props: ["row"],
    data: function () {
            return {
            }
        },
    methods: {
        onProcess(oldT, newT) {
            HTTP.post(
                "ProcessReconciliation/",
                querystring.stringify({
                    reconciliation_id: this.row.id,
                    transaction1_id: this.row.transaction1.id,
                    transaction1_keep: oldT,
                    transaction2_id: this.row.transaction2.id,
                    transaction2_keep: newT}))
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