function addPieChart1(){
  new Chart(document.getElementById("pie-chart-1"), {
      type: 'pie',
      data: {
        labels: ["Dep1", "Dep2", "Dep3", "Dep4", "Dep5"],
        datasets: [{
          label: "Population (millions)",
          backgroundColor: ["rgba(84,161,229,1.0)","rgba(108,190,191,1.0)","rgba(248,206,107,1.0)","rgba(242,162,84,1.0)","rgba(237,110,133,1.0)"],
          data: [2478,5267,734,784,433]
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

function addPieChart2(){
  new Chart(document.getElementById("pie-chart-2"), {
      type: 'pie',
      data: {
        labels: ["Medium", "Critical", "High", "Low", "None"],
        datasets: [{
          label: "Population (millions)",
          backgroundColor: ["rgba(255,232,161,1.0)","rgba(180,71,84,1.0)","rgba(248,206,107,1.0)","rgba(242,162,84,1.0)","rgba(237,110,133,1.0)"],
          data: [343,768,235,666,478]
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
