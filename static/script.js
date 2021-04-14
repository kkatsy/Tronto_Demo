
function clearForm() {
  // remove user input, clear results, hide containers
  //document.getElementById("appNameFormInput").value = "";
  $('#dependencyTagsInput').tagsinput('removeAll');
  document.getElementById("result").innerHTML = "";
  //$(":checkbox").prop('checked', false).parent().removeClass('active');

  if(document.getElementById("not-in-onto") != null){
    document.getElementById("not-in-onto").innerHTML = "";
  }
  if(document.getElementById("tweetError") != null){
    document.getElementById("tweetError").innerHTML = "";
  }

  $('#navTabs').addClass('hidden');
  $("#chatbotContainer").addClass('hidden');
  $('#chatbotChat').empty();
  restartChat();
  $('.nav-tabs a[href="#tableTab"]').tab('show');

  $('#spinnerContainer').removeClass('spinner');
  $('#dependencyTable').addClass('hidden');
  $('#tweet-container').addClass('hidden');
  $('#resultContainer').addClass('hidden');

  $("#dependencyTable tr").remove();
  $("#tweet-container div").remove();
  document.querySelector("#pieChart1").innerHTML = 'CVEs per Dependency<canvas id="pie-chart-1"></canvas>';
  document.querySelector("#pieChart2").innerHTML = 'Severity Distribution<canvas id="pie-chart-2"></canvas>';
}

function addTypeahead() {
  // get JSON keys for typeahead plugin
  var dependencynames = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    prefetch: {
      url: 'dependencynames.json',
      filter: function(list) {
        return $.map(list, function(dependencyname) {
          return { name: dependencyname }; });
      }
    }
  });
  dependencynames.initialize();

  $('input').tagsinput({
    typeaheadjs: {
      name: 'dependencynames',
      displayKey: 'name',
      valueKey: 'name',
      source: dependencynames.ttAdapter()
    }
  });
}

function generateTableHead(table, data) {
  let thead = table.createTHead();
  let row = thead.insertRow();
  for (let key of data) {
    let th = document.createElement("th");
    let text = document.createTextNode(key);
    th.appendChild(text);
    row.appendChild(th);
  }
}

function generateTable(table, data) {
  for (let element of data) {
    let row = table.insertRow();
    for (key in element) {
      let cell = row.insertCell();
      let text = document.createTextNode(element[key]);
      cell.appendChild(text);
    }
  }
}

function createTweets(tweet_list){
  for(let tweet_ID of tweet_list){
    twttr.widgets.createTweet(
    tweet_ID,
    document.getElementById('tweet-container'),
    {
      conversation : 'none',    // or all
      cards        : 'hidden',  // or visible
      linkColor    : '#cc0000', // default is blue
      theme        : 'light'    // or dark
    }
    );
  }
}

function showStatus(app_name, vulnerability_status, severity){
  // vulnerable or not vulnerable
  document.getElementById("result").innerHTML = "Your application " + app_name + " is " + vulnerability_status + "!";

  if(vulnerability_status == "vulnerable"){
    $("#result").addClass("bg-danger");
    document.getElementById("result").innerHTML = document.getElementById("result").innerHTML + "<br>" + "Severity level: " + severity;
    document.getElementById("result").style.color = "rgba(180,71,84,1.0)";
  } else {
    $("#result").addClass("bg-success");
    document.getElementById("result").style.color = "rgba(39, 142, 32,1.0)";
  }

  $("#resultContainer").removeClass('hidden');
}

// function showIfCritical(critical_status){
//   if(critical_status == "true"){
//     document.getElementById("warning-result").innerHTML = "WARNING: One or more dependencies have CRITICAL vulnerabilities!"
//   } else {
//     document.getElementById("warning-result").innerHTML = ""
//   }
// }

function showDependencyData(dependency_dict, not_in_onto){
  // add if some dependencies on in system
  if(not_in_onto.length > 0){
    not_in_onto_list = not_in_onto.toString();
    document.getElementById("not-in-onto").innerHTML = "Entered dependencies that are not in our system: " + not_in_onto_list;
  }

  // create table with data for dependencies
  dependencies = dependency_dict
  let table = document.querySelector("table");
  let data = Object.keys(dependencies[0]);
  generateTable(table, dependencies);
  generateTableHead(table, data);
  $("#dependencyTable").removeClass('hidden');
}

function showTweets(query_list){
  if(query_list.length > 21){
    query_list = query_list.slice(0,20);
  }

  var json_query = JSON.stringify(query_list);
  json_query = encodeURIComponent(json_query);

  // get site route for app status func server-side
  var url = "/tweet_ids/" + json_query;

  // get request to get application's vuln status
  var http = new XMLHttpRequest();
  http.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

      var response = this.responseText;
      if(response == "error"){
        console.log(response)
      } else {
        var tweet_list = JSON.parse(response)
        if (tweet_list.length > 0) {
          createTweets(tweet_list);
          $("#tweet-container").removeClass('hidden');
        } else {
          console.log("no tweets to display")
          document.getElementById("tweetError").innerHTML = "No recent vulnerability-related tweets found.";

        }

      }

    }
  }
  http.open("GET", url, true);
  http.send();
}

function getAppData(input){
  // get site route for app data func server-side
  //console.log("input_json: ", input_json)
  var input_json = encodeURIComponent(input);
  var url = "/app_data/" + input_json;

  // get request to get application's vuln status
  var http = new XMLHttpRequest();
  http.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

      var response = this.responseText;
      response = JSON.parse(response)
      //console.log("response: ", response)

      if(response.vulnerabilities.length > 0){
        // call functions to display received app data
        showStatus("", response.is_vulnerable, response.is_critical);
        showDependencyData(response.dependency_dict, response.not_in_onto);
        showTweets(response.vulnerabilities);

        if(response.not_in_onto.length > 0){
          console.log(response.not_in_onto)
        }

        $('#spinnerContainer').removeClass('spinner');
        $("#navTabs").removeClass('hidden');
        $("#chatbotContainer").removeClass('hidden');

        addPieChart1(response.dependency_dict);
        addPieChart2(response.dependency_dict);
      }
    } else if (this.status == 404) {
      console.log("404 error")
    }

  }
  http.open("GET", url, true);
  http.send();
}

function clickCheck() {
  if($("#dependencyTagsInput").val() != ""){
    // hide all results containers, start spinner
    $('#spinnerContainer').addClass('spinner');
    $("#dependencyTable").addClass('hidden');
    $("#tweet-container").addClass('hidden');
    $("#resultContainer").addClass('hidden');
    $("#navTabs").addClass('hidden');
    $("#chatbotContainer").addClass('hidden');

    // clear prev output in case of updated input
    $("#dependencyTable tr").remove();
    $("#tweet-container div").remove();

    document.querySelector("#pieChart1").innerHTML = 'CVEs per Dependency<canvas id="pie-chart-1"></canvas>';
    document.querySelector("#pieChart2").innerHTML = 'Severity Distribution<canvas id="pie-chart-2"></canvas>';

    // get application name
    //name = document.getElementById("appNameFormInput").value

    // get dependencies, split into list
    depend_string = $("#dependencyTagsInput").val()
    var depend_string = depend_string.split(',');

    // get json string w dependencies
    var obj = new Object();
    obj.name = "";
    obj.dependencies = depend_string;

    // checkbox = $("#embedCheck:checked").val()
    // if (checkbox == "on") {
    //   obj.embed = "true";
    // } else {
    //   obj.embed = "false";
    // }

    // func to make http request for app's data
    var app_json_string = JSON.stringify(obj);
    //console.log(app_json_string);
    getAppData(app_json_string);
  }
}
