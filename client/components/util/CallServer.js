export default {
    data() {
        return {
            axios: null,
            querystring: null,
            apiUrl: "http://127.0.0.1:5000/",
            allData: null,
            RunningBalance: null,
        };
    },
    mounted() {
        this.axios = require("axios");
        this.querystring = require("querystring");
    },
    methods: {
        getAllData(api, params) {
            this.axios
                .get(this.apiUrl + api + "/" + params)
                .then(response => {
                    this.allData = response["data"]["data"];
                })
                .catch(function (error) {
                    console.log(error);
                });
        },
        getRunningBalance(fromDate) {
            let params = {};
            if (fromDate) params["byDate"] = fromDate;
            this.axios
                .get(this.apiUrl + "RunningBalance/" + "?filter=" + JSON.stringify(params))
                .then(response => {
                    this.RunningBalance = response["data"]["data"][0]['balance'];
                })
                .catch(function (error) {
                    console.log(error);
                });
        }
    }
}