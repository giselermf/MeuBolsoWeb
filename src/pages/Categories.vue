<template>
  <main-layout>
    <h1>Categories</h1>
    <div id="app" class="ui vertical stripe segment">
        <category-edit 
            :category_id="selected_id"
            :category="selected_category" 
            :description="selected_description"> 
        </category-edit>
    </div>
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

  </main-layout>
</template>

<script>
  import axios from 'axios';
  import MainLayout from '../layouts/Main'
  import CategoryEdit from '../components/Category/CategoryEdit'
  import MyVuetable from '../components/MyVuetable'

  export default {
    components: {
      MainLayout,CategoryEdit, MyVuetable
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
                        name: 'Description',
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
                    field: 'Category',
                    sortField: 'Category',
                    direction: 'asc'
                    }
                ],
                moreParams: {},
	        }
        },
    methods: {
            onDelete(data) {
                var axios = require('axios');
                axios.delete('http://127.0.0.1:5000/categories/'+data.id, {
                    headers: {
                        'id': this.category_id,
                        'Content-Type': 'application/json'
                    }
                }).then((response) => {
                    this.$events.fire('filter-reset')
                })
                .catch(function (error) {
                    console.log(error);
                });
            }, 
	        onEdit (data) {
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
</syle>


