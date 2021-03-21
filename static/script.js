
function clearForm() {

  document.getElementById("appNameFormInput").value = "";
  $('#dependencyTagsInput').tagsinput('removeAll');
  document.getElementById("result").innerHTML = "";
  //$(":checkbox").prop('checked', false).parent().removeClass('active');

  if(document.getElementById("warning") != null){
    document.getElementById("warning").innerHTML = "";
  }

  // remove previous results
  $('#spinnerContainer').removeClass('spinner');
  $('#dependencyTable').addClass('hidden');
  $('#tweet-container').addClass('hidden');
  $('#resultContainer').addClass('hidden');
  $("#dependencyTable tr").remove();
  $("#tweet-container div").remove();
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

function showStatus(app_name, vulnerability_status){
  document.getElementById("result").innerHTML = "Your application " + app_name + " is " + vulnerability_status + "!";
  $("#resultContainer").removeClass('hidden');
}

function showIfCritical(critical_status){
  if(critical_status == "true"){
    document.getElementById("warning-result").innerHTML = "WARNING: One or more dependencies have CRITICAL vulnerabilities!"
  } else {
    document.getElementById("warning-result").innerHTML = ""
  }
}

function showDependencyData(dependency_dict){
  dependencies = dependency_dict
  let table = document.querySelector("table");
  let data = Object.keys(dependencies[0]);
  generateTable(table, dependencies);
  generateTableHead(table, data);
  $("#dependencyTable").removeClass('hidden');
}

function showTweets(query_list){
  json_query = JSON.stringify(query_list)

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
        createTweets(tweet_list);
        $('#spinnerContainer').removeClass('spinner');
        $("#tweet-container").removeClass('hidden');
      }

    }
  }
  http.open("GET", url, true);
  http.send();
}

function getAppData(input_json){
  // get site route for app status func server-side
  var url = "/app_data/" + input_json;

  // get request to get application's vuln status
  var http = new XMLHttpRequest();
  http.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

      var response = this.responseText;
      response = JSON.parse(response)
      console.log("response: ", response)

      showStatus(response.name, response.is_vulnerable);
      showIfCritical(response.is_critical);
      showDependencyData(response.dependency_dict);
      showTweets(response.vulnerabilities);
    }
  }
  http.open("GET", url, true);
  http.send();
}

function clickCheck() {

  // hide all results containers, start spinner
  $('#spinnerContainer').addClass('spinner');
  $("#dependencyTable").addClass('hidden');
  $("#tweet-container").addClass('hidden');
  $("#resultContainer").addClass('hidden');

  // clear prev output in case of updated input
  $("#dependencyTable tr").remove()
  $("#tweet-container div").remove()

  // get application name
  name = document.getElementById("appNameFormInput").value

  // get dependencies, split into list
  depend_string = $("#dependencyTagsInput").val()
  var depend_string = depend_string.split(',');

  // get json string w dependencies
  var obj = new Object();
  obj.name = name;
  obj.dependencies = depend_string;

  // checkbox = $("#embedCheck:checked").val()
  // if (checkbox == "on") {
  //   obj.embed = "true";
  // } else {
  //   obj.embed = "false";
  // }

  var app_json_string = JSON.stringify(obj);
  console.log(app_json_string);

  getAppData(app_json_string);
}
