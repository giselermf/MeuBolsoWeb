export function filter(arr, criteria) {
  return arr.filter(function(obj) {
    return Object.keys(criteria).every(function(c) {
      return obj[c] == criteria[c];
    });
  });
};

export function getUrlFilters(year_filters, type_filters, category_filters, subcategory_filters, account_filters) {
  let filters = '';
  if (year_filters != null && year_filters != '')
    filters += '&year_filter='+year_filters;
  if (type_filters != null && type_filters != '') 
    filters += '&type_filter='+type_filters;
  if (category_filters != null && category_filters != '')
    filters += '&category_filter='+category_filters;
  if (subcategory_filters != null && subcategory_filters != '')
    filters += '&subcategory_filter='+subcategory_filters;
  if (account_filters != null && account_filters != '')
    filters += '&account_filters='+account_filters;
  return filters;
};

export function getChartData (response, xLabel, datasetLabel) {
    let datasets = [];
    let values = [];
    let backgroundCollors = ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"];

    let labels = [new Set(response.map(item => item[xLabel]))];
    labels = Array.from(labels[0]);

    let datasetLabels = [new Set(response.map(item => item[datasetLabel]))];
    //sort if Date
    datasetLabels = Array.from(datasetLabels[0]).sort(function(a,b) {
        a = a.split('/').reverse().join('');
        b = b.split('/').reverse().join('');
        return a > b ? 1 : a < b ? -1 : 0;
      });

    datasetLabels.forEach(function(aDataset) { 
      values = [];
      labels.forEach(function(oneLabel){
          let filterMap = {};
          filterMap[datasetLabel] = aDataset;
          filterMap[xLabel] = oneLabel;
          let result = filter(response, filterMap);
          let total = 0;
          if (result[0] != undefined) {
             total = result[0]['Total'];  
          } 
          values.push(total);
          
        }, this);
        datasets.push(
          {
            label: aDataset,
            borderWidth: 1,
            backgroundColor: backgroundCollors[datasets.length % backgroundCollors.length],
            data: values
          });
              
    }, this);
    let chartData = {
      labels: labels,
      datasets: datasets
    };
    return chartData;
}