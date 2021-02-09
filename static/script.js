
function showInput() {
  // check that things are working
  name = document.getElementById("dependencyTagsInput").tagsinput('items')
  var split = name.split(',');
  url = "/helloworld/" + split;
  var http = new XMLHttpRequest();
  http.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      // var response = JSON.parse(this.responseText)
      var response = this.responseText;
      document.getElementById("result").innerHTML = response;
    }
  }
  http.open("GET", url, true);
  http.send();
}


function clearForm() {
  // clear form input and output
  document.getElementById("appNameFormInput").value = "";
  $('#dependencyTagsInput').tagsinput('removeAll');
  document.getElementById("result").innerHTML = "";
  $(":checkbox").prop('checked', false).parent().removeClass('active');

}


function add_typeahead() {
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


function generate_table(response){

  var dependencies = JSON.parse(response);

  let table = document.querySelector("table");
  let data = Object.keys(dependencies[0]);
  generateTable(table, dependencies);
  generateTableHead(table, data);
}


function showTable() {

  url = "/dependency_statuses";
  var http = new XMLHttpRequest();

  http.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

      var response = this.responseText;
      $("#dependencyTable").removeClass('hidden');
      generate_table(response);
    }
  }
  http.open("GET", url, true);
  http.send();

}


function transferJSON() {
  // get application name
  name = document.getElementById("appNameFormInput").value

  // get dependencies, split into list
  depend_string = $("#dependencyTagsInput").val()
  var depend_string = depend_string.split(',');

  checkbox = $("#embedCheck:checked").val()

  // get json string w dependencies
  var obj = new Object();
  obj.name = name;
  obj.dependencies = depend_string;
  obj.status = "unknown";

  if (checkbox == "on") {
    obj.embed = "true";
  } else {
    obj.embed = "false";
  }

  var json_string = JSON.stringify(obj);

  // get site route for app status func server-side
  var url = "/app_status/" + json_string;

  // get request to get application's vuln status
  var http = new XMLHttpRequest();
  http.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

      var response = this.responseText;
      document.getElementById("result").innerHTML = "Your application " + name + " is " + response + "!";

      showTable();
    }
  }
  http.open("GET", url, true);
  http.send();
}
