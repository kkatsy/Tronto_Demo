function addPieChart1(data_dict){
  // collect dependencies + number of CVEs in each dependency
  var dependency_names = [];
  var num_vulnerabilities = [];
  for (var i = 0; i < data_dict.length; i++) {
    depend_name = data_dict[i].Name;
    dependency_names.push(depend_name);

    vuln_str = data_dict[i].Vulnerabilities;
    vuln_list = vuln_str.split(", ");
    vuln_num = vuln_list.length
    num_vulnerabilities.push(vuln_num);
  }

  var colors = ["rgba(84,161,229,1.0)","rgba(108,190,191,1.0)", "rgba(163, 228, 215, 1.0)", "rgba(19, 141, 117, 1.0)", "rgba(125, 206, 160, 1.0)", "rgba(195, 155, 211, 1.0)"]
  new Chart(document.getElementById("pie-chart-1"), {
      type: 'pie',
      data: {
        labels: dependency_names,
        datasets: [{
          label: "Population (millions)",
          backgroundColor: colors,
          data: num_vulnerabilities
        }]
      },
      options: {
          title: {
              display: true,
              text: 'Custom Chart Title'
          }
      }
  });
}

function addPieChart2(data_dict){
  console.log(data_dict)
  var none = 0;
  var low = 0;
  var medium = 0;
  var high = 0;
  var critical = 0;
  for (var i = 0; i < data_dict.length; i++) {
    severity = data_dict[i].Severity;
    if(severity == 'none'){
      none = none + 1;
    }
    if(severity == 'low'){
      low = low + 1;
    }
    if(severity == 'medium'){
      medium = medium + 1;
    }
    if(severity == 'high'){
      high = high + 1;
    }
    if(severity == 'critical'){
      critical = critical + 1;
    }
  }

  data = [none, low, medium, high, critical];
  colors = ["rgba(255,232,161,1.0)","rgba(248,206,107,1.0)","rgba(242,162,84,1.0)","rgba(237,110,133,1.0)","rgba(180,71,84,1.0)"];
  new Chart(document.getElementById("pie-chart-2"), {
      type: 'pie',
      data: {
        labels: ["None", "Low", "Medium", "High", "Critical"],
        datasets: [{
          label: "Population (millions)",
          backgroundColor: colors,
          data: data
        }]
      },
      options: {
          title: {
              display: true,
              text: 'Custom Chart Title'
          }
      }
  });
}
