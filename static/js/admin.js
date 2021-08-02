// $( document ).ready(function() {

htmlString = '<h5>Action</h5><ul class="list-group">' 
var adminSideBar = ['User', 'Data', 'News', 'Place', 'Unesco_Site']
$.each(adminSideBar, function( index, value ) {
    htmlString += '<a id="'+value+'"><li class="list-group-item">' + value + '</li></a>';
  });
htmlString += '</ul>'
$('#sidebar').html(htmlString);

function makeAjaxRequest(url, data, method, async=true)
{
    var ret = {}
    $.ajax({
        url: url,
        asysc:async,
        data: data,
        contentType: false,
        processData: false,
        type: method,
        success: function(data){
            alert(data['msg']);
        },
        error: function (xhr, ajaxOptions, thrownError) {
            ret["data"] = xhr.status + thrownError;
            alert(ret["data"]);
          }
    });
}

var addUserForm = `
  <div class="form-outline mb-4">
  <label class="form-label" for="email" required>Email address</label>
  <input type="text" id="email" class="form-control" />
  </div>
  <div class="form-outline mb-4">
  <label class="form-label" for="password">Password</label>
  <input type="password" id="password" class="form-control" required />
  </div>`;

var addNewsForm = `
  <div class="form-outline mb-4">
    <label class="form-label" for="newsTag">News Tag</label>
    <input type="text" id="newsTag" class="form-control" required />
  </div>

  <div class="form-outline mb-4">
    <label class="form-label" for="newsHeading">News Heading</label>
    <input type="text" id="newsHeading" class="form-control" required />
  </div>`;

var addPlaceForm = `<div class="form-outline mb-4">
    <label class="form-label" for="district">District</label>
    <input type="text" id="district" class="form-control" required />
  </div>

  <div class="form-outline mb-4">
    <label class="form-label" for="state">State</label>
    <input type="text" id="state" class="form-control" required />
  </div>

  <div class="row mb-4">
    <div class="col">
      <div class="form-outline">
      <label class="form-label" for="lat">Lattitude</label>
      <input  type="number" step="0.01" min="0" id="lat" class="form-control" required />
      </div>
    </div>
    <div class="col">
      <div class="form-outline">
      <label class="form-label" for="long">Longitude</label>
      <input  type="number" step="0.01" min="0" id="long" class="form-control" required />
      </div>
    </div>
  </div>`;


  var addUnescoForm = `<div class="form-outline mb-4">
  <label class="form-label" for="unesco_site_name">UNESCO Site Name</label>
  <input type="text" id="unesco_site_name" class="form-control" required />
  </div>

  <div class="form-outline mb-4">
  <label class="form-label" for="district">District</label>
  <input type="text" id="district" class="form-control" required />
  </div>

<div class="form-outline mb-4">
  <label class="form-label" for="state">State</label>
  <input type="text" id="state" class="form-control" required />
</div>`;

var addCovidDataForm = `
<div class="form-outline mb-4">
<label class="form-label" for="district">District</label>
<input type="text" id="district" class="form-control" required />
</div>

<div class="form-outline mb-4">
<label class="form-label" for="active_cases">Active Cases</label>
<input type="number" step="1" min="0" id="active_cases" class="form-control" required />
</div>

<div class="form-outline mb-4">
<label class="form-label" for="active_cases_date">Report Date</label>
<input type="date" id="active_cases_date" class="form-control" required />
</div>
`;

var serchKeys;

function matchedList(place)
    {
        htmlString = '<ul class="placeSuggestion" style="background-color:#00d4d4; position:absolute; width:300px;list-style-type:none;margin-left:0;">';
        $.each(serchKeys, function( index, value ) {
            place = place.toUpperCase();
            value1 = value.toUpperCase();            
            if(value1.startsWith(place))
            {
            htmlString += '<li id = "'+value+'" onclick="foundPlace(this, '+value+')">' + value + '</li>';
            }
          });

        htmlString += '</ul>';
        return htmlString; 
    }

    function foundPlace(obj,abc)
    {
       console.log("in here")
        var id = $(abc).attr('id');
        $('#suggestion').val($(obj).text());
        
        $('#suggestionList').fadeOut();
       $('#suggestionList').html("");

    }

$('#suggestion').keyup(function(){
  var place = $(this).val();
  if(place != '')
  {
      $('#suggestionList').fadeIn();
      $('#suggestionList').html(matchedList(place));
  }
  else
  {
      $('#suggestionList').fadeOut();
      $('#suggestionList').html("");
  }
  });

function place_side_bar(url)
{
      $.ajax({
        url: url,
        contentType: false,
        processData: false,
        type: 'POST',
        success: function(data){
          serchKeys = data['list'];
          // console.log(serchKeys);
      },
      error: function (xhr, ajaxOptions, thrownError) {
          ret = xhr.status + thrownError;
          alert(ret);
        }
  });
}

$('#User').click(function(){
    $('#deleteBox').show();
    $('#suggestionList').html("");
    $('#selected_action').text("Create New Admin");
    $("#adminForm").empty();
    var parser = new DOMParser()
    var f = parser.parseFromString(addUserForm, "text/html").body;
    document.getElementById("adminForm").appendChild(f);
    document.getElementById('adminFromSubmit').innerHTML = "Create User"
    document.getElementById('adminFromSubmit').value = "user_create"
    place_side_bar('getUserDataList')
    document.getElementById('deleteField').value = 'user';

});

$('#News').click(function(){
    $('#deleteBox').show();
    $('#suggestionList').html("");

    $('#selected_action').text("News");
    $("#adminForm").empty();
    var parser = new DOMParser()
    var f = parser.parseFromString(addNewsForm, "text/html").body;
    document.getElementById("adminForm").appendChild(f);
    document.getElementById('adminFromSubmit').innerHTML = "Update"
    document.getElementById('adminFromSubmit').value = "news_update"
    place_side_bar('getNewsDataList');
    document.getElementById('deleteField').value = 'news';
});

$('#Place').click(function(){
    // console.log("In Place ");
    $('#deleteBox').show();
    $('#suggestionList').html("");

    $('#selected_action').text("Place Action");
    $("#adminForm").empty();
    var parser = new DOMParser()
    var f = parser.parseFromString(addPlaceForm, "text/html").body;
    document.getElementById("adminForm").appendChild(f);
    document.getElementById('adminFromSubmit').innerHTML = "Create"
    document.getElementById('adminFromSubmit').value = "place_create";
    place_side_bar('getPlaceDataList');
    document.getElementById('deleteField').value = 'place';

});

$('#Unesco_Site').click(function(){
  $('#deleteBox').show();
  $('#suggestionList').html("");

  $('#selected_action').text("UNESCO Site Action");
    $("#adminForm").empty();
    var parser = new DOMParser()
    var f = parser.parseFromString(addUnescoForm, "text/html").body;
    document.getElementById("adminForm").appendChild(f);
    document.getElementById('adminFromSubmit').innerHTML = "Create"
    document.getElementById('adminFromSubmit').value = "unesco_create"
    place_side_bar('getUnescoDataList');
    document.getElementById('deleteField').value = 'unesco';


});


$('#Data').click(function(){
  $('#deleteBox').hide();
  $('#suggestionList').html("");
  $('#selected_action').text("Insert New Covid Data");
    $("#adminForm").empty();
    var parser = new DOMParser()
    var f = parser.parseFromString(addCovidDataForm, "text/html").body;
    document.getElementById("adminForm").appendChild(f);
    document.getElementById('adminFromSubmit').innerHTML = "Insert"
    document.getElementById('adminFromSubmit').value = "covid_insert"
    document.getElementById('deleteField').value = 'data';

});


$('#adminFromSubmit').click(function(event){
    event.preventDefault();
    var name = document.getElementById('adminFromSubmit').value;
    var fd = new FormData();
    var url;
    if (name == 'user_create')
    {
        // console.log(name);
        var uname = document.getElementById("email").value;
        var psw =   document.getElementById("password").value;
        fd.append("uname", uname)
        fd.append("psw", psw)
        url = 'createUser'
    }
    else if(name == 'news_update')
    {
        // console.log(name);
        var fd = new FormData();
        var newsTag = document.getElementById("newsTag").value;
        var newsHeading = document.getElementById("newsHeading").value;
        fd.append("newsTag", newsTag)
        fd.append("newsHeading", newsHeading)
        // console.log(fd)
        url = 'createNews'

    }
    else if(name == 'place_create')
    {
        var district = document.getElementById("district").value;
        var state =   document.getElementById("state").value;
        var lat = document.getElementById("lat").value;
        var longi =   document.getElementById("long").value;
        fd.append("district", district)
        fd.append("state", state)
        fd.append("lat", lat)
        fd.append("longi", longi)
        url = 'createPlace'
    }
    else if(name == 'unesco_create')
    {
      var unesco_site_name = document.getElementById("unesco_site_name").value;
      var district = document.getElementById("district").value;
      var state =   document.getElementById("state").value;
      
      fd.append("unesco_site_name", unesco_site_name)
      fd.append("district", district)
      fd.append("state", state)
      url = 'createUnesco'
    }
    else if(name == 'covid_insert')
    {
      var district = document.getElementById("district").value;
      var active_cases =   document.getElementById("active_cases").value;
      var active_cases_date =   document.getElementById("active_cases_date").value;

      fd.append("district", district)
      fd.append("active_cases", active_cases)
      fd.append("active_cases_date", active_cases_date)
      url = 'insertActiveCases'
    }
    makeAjaxRequest(url, fd,'POST');
    });

    $('#deleteButton').click(function(){
      var type = document.getElementById('deleteField').value;
      var key = document.getElementById('suggestion').value;
      var fd = new FormData();
      fd.append("type", type);
      fd.append("key", key);
      console.log("hhhhhhhhhhhhhhh ", type, " ", key);

      $.ajax({
        url: 'deleteFiled',
        data: fd,
        contentType: false,
        processData: false,
        type: 'POST',
        success: function(data){
            keys = []
            $.each(serchKeys, function( index, value )
            {
              if (value != key) keys.append(value);
            });
            serchKeys = keys;

            alert(data['msg']);
        },
        error: function (xhr, ajaxOptions, thrownError) {
            ret["data"] = xhr.status + thrownError;
            alert(ret["data"]);
          }
    });
    })
$('#User').click();
// });