<template>
    <div id="app" class="ui vertical stripe segment">
        <div id="content" class="ui basic segment">
        <my-vuetable ref="vuetable"
                api-url="http://127.0.0.1:5000/transactions/"
                :fields="fields"
                :sort-order="sortOrder"
                :append-params="moreParams"
            >
                <template slot="actions" scope="props">
                    <a style="font-size: 20px; padding-right: 11px;cursor:pointer" @click="onEdit(props.rowData)">&#10000;</a>
                </template>
            </my-vuetable>
        </div>
    </div>
</template>

<script>
  import axios from 'axios';
  import MyVuetable from './/MyVuetable'

  export default {
    components: {
      MyVuetable
    },
    data () {
        return {
            selected_id: '',
            selected_category: '',
            selected_description: '',
            fields: [ 
                    {
                        name: 'id',
                        titleClass: 'center aligned',
                        dataClass: 'center aligned',
                    },
                    {
                        name: 'Category',
                        titleClass: 'center aligned',
                        dataClass: 'center aligned',
                    },
                    {
                        name: 'SubCategory',
                        titleClass: 'center aligned',
                        dataClass: 'center aligned',
                    },
                    {
                        name: 'Currency',
                        titleClass: 'center aligned',
                        dataClass: 'center aligned',
                    },
                    {
                        name: 'Amount',
                        titleClass: 'center aligned',
                        dataClass: 'center aligned',
                    },
                    {
                        name: 'Date',
                        titleClass: 'center aligned',
                        dataClass: 'center aligned',
                    },
                    {
                        name: '__slot:actions',
                        title: 'Slot Actions',
                        titleClass: 'center aligned',
                        dataClass: 'center aligned',
                    }
                ],
                sortOrder: [
                    {
                    field: 'Category',
                    sortField: 'Category',
                    direction: 'asc'
                    }
                ],
                moreParams: {},
	        }
        },
    methods: {
	        onEdit (data) {
                this.$events.fire('edit-record', data)
            }
    }
  }
</script>

<style>
.ui.table td {
    padding: 1px;
}
</style>


