export let colors = ["Red", "Green","Blue", "Yellow", "Purple", 
"Orange", "Grey", "Pink", "OrangeRed", "Lime", "Tomato", "CadetBlue", "Steelblue", "Magenta", "Brown", "Chocolate"]

export function getDatasetColors(values) {
  let datasetColors = [];
  for (let index in values) {
    datasetColors.push(colors[index % colors.length]);
  }
  return datasetColors;
};  

export function addFilterParam(allPossibleFilters) {
  let filterParams = {};
  Object.keys(allPossibleFilters).forEach(function(key,index) {
    let filterValue = allPossibleFilters[key];
    if (filterValue != null && filterValue.length > 0)
      filterParams[key] = filterValue;
  });
  return filterParams;
};

export function groupDataBy(all_data, grouper) {
  let data = all_data.reduce(function(r, a) {
    r[a[grouper]] = r[a[grouper]] || 0;
    r[a[grouper]] += a["AmountEUR"];
    return r;
  }, Object.create(null));
  return {
    labels: Object.keys(data),
    values_negatives: Object.values(data).map(x => { if (x<0) return Math.round(Math.abs(x)  )}),
    values_positives: Object.values(data).map(x => { if (x>0) return Math.round(x) })
  };
};

export function getDataSetPie(labels, values) {
  return {
    labels: labels,
    datasets: [
      {
        label: "Data One",
        pointBackgroundColor: "white",
        borderWidth: 1,
        pointBorderColor: "white",
        backgroundColor: getDatasetColors(values),
        data: values
      }
    ]
  };
};

export function getGroupByMonthAnd(all_data, groupByOther) {
  let xLabel = "yearmonth";
  let datasetLabel = groupByOther;

  //group by year and month
  let groupedData = all_data.reduce(function (r, a) {
    r[a["Year"] + "/" + a["Month"]] = r[a["Year"] + "/" + a["Month"]] || [];
    r[a["Year"] + "/" + a["Month"]].push(a);
    return r;
  }, Object.create(null));

  //group "groupByOther" 
  for (let e in groupedData) {
    groupedData[e] = groupedData[e].reduce(function (r, a) {
      r[a[groupByOther]] = r[a[groupByOther]] || [];
      r[a[groupByOther]].push(a);
      return r;
    }, Object.create(null));
  }

  // calculate grandTotal by yearmonth and "groupByOther"
  for (let e in groupedData) {
    for (let x in groupedData[e]) {
      let grandTotal = 0;
      {
        for (let r in groupedData[e][x]) {
          grandTotal += groupedData[e][x][r]["AmountEUR"]
        }
      }
      groupedData[e][x] = Math.round(grandTotal);
    }
  }
  return groupedData;
};

export function getLabelAndDatabaseBar(groupedData, datasetColors) {
  let labels = [];
  let datasetLabels = [];
  let datasets = [];

// get labels and datasetLabels (x values)
  for (let e in groupedData) {
    for (let x in groupedData[e]) {
      if (!labels.includes(e)) labels.push(e);
      if (!datasetLabels.includes(x)) datasetLabels.push(x);
    }
  }
  //sort datasetLabels (yearmonth)
  datasetLabels = datasetLabels.sort(function (a, b) {
    a = a.split("/").reverse().join("");
    b = b.split("/").reverse().join("");
    return a > b ? 1 : a < b ? -1 : 0;
  });

  datasetLabels.forEach(function (aDataset) {
    let values = [];
    labels.forEach(function (oneLabel) {
      values.push(groupedData[oneLabel][aDataset] || 0);
    }, this);
    datasets.push({
      label: aDataset,
      borderWidth: 1,
      beginzero: "true",
      fill: false,
      backgroundColor: datasetColors[datasets.length % colors.length],
      data: values
    });
  }, this);

  return {
    labels: labels,
    datasets: datasets
  };
}
