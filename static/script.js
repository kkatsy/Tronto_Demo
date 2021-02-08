function transferJSON() {
  // get dependencies, split into list
  name = document.getElementById("appNameFormInput").value

  //depend_string = document.getElementById("dependencyTagsInput").tagsinput('items')
  depend_string = $('#dependencyTagsInput').val()

  var depend_string = depend_string.split(',');

  // get json string w dependencies
  var obj = new Object();
  obj.name = name;
  obj.dependencies = depend_string;
  obj.status = 'unknown';
  var json_string = JSON.stringify(obj);

  // get site route for app status func server-side
  var url = "/app_status/" + json_string;

  // get request to get application's vuln status
  var http = new XMLHttpRequest();
  http.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var response = this.responseText;
      document.getElementById("result").innerHTML = "Your program is " + response + ".";
    }
  }
  http.open("GET", url, true);
  http.send();
}


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

// TODO
function create_table() {}
