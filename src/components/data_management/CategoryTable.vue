<template>
    <div id="app" class="ui vertical stripe segment">
        <div class="ui container">
            <div id="content" class="ui basic segment">
            <my-vuetable ref="vuetable"
                  api-url="http://127.0.0.1:5000/categories/"
                  :fields="fields"
                  :sort-order="sortOrder"
                  :append-params="moreParams"
                >
                    <template slot="actions" scope="props">
                        <a style="font-size: 20px; padding-right: 11px;cursor:pointer" @click="onEdit(props.rowData)">&#10000;</a>
                        <a style="cursor:pointer" @click="onDelete(props.rowData)"> &#10060;</a>
                    </template>
                </my-vuetable>
            </div>
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
                        name: 'category',
                        titleClass: 'center aligned',
                        dataClass: 'center aligned',
                    },
                    {
                        name: 'description',
                        titleClass: 'center aligned',
                        dataClass: 'center aligned',
                        callback: 'formatDescription'
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
                    field: 'category',
                    sortField: 'category',
                    direction: 'asc'
                    }
                ],
                moreParams: {},
	        }
        },
    methods: {
	        onEdit (data) {
                this.$events.fire('edit-record', data)
               this.selected_id = data.id
                this.selected_category = data.Category
                this.selected_description = data.Description 
            }
    }
  }
</script>

<style>
.ui.table td {
    padding: 1px;
}
</style>


