// $( document ).ready(function() {
    
    var srcCity = document.getElementById("srcCity");
    var desCity = document.getElementById("destCity");



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
                ret["status"] = "pass";
                ret["data"] = data;
                return ret;
            },
            error: function (xhr, ajaxOptions, thrownError) {
                ret["status"] = "fail";
                ret["data"] = xhr.status + thrownError;
                return ret;
              }
        });
    }

    $('#form1submit').click(function(event){
        event.preventDefault();
        $("#mapArea").empty();
        $("#mapArea").addClass("loader");
        var fd = new FormData();
        fd.append("srcCity", srcCity.value)
        fd.append("destCity", destCity.value)
        if(srcCity.value == destCity.value)
            {
                alert('Source place and destination Place are same !!')
                return;
            }
        $.ajax({
            url: '/page',
            data: fd,
            contentType: false,
            processData: false,
            type: 'POST',
            success: function(data){
                $("#mapArea").removeClass("loader");
                foundPath = ""
                // console.log(data['foundPath'])
                // $.each(data['foundPath'], function( index, value ) {
                //     foundPath += value + '-->'
                //   });
                                
                st = ' width="800" height="600" frameborder="0" style="border:0"';
                urlStr = '<iframe src="'+ data["url"] + '" '+st+'> </iframe>';
                document.getElementById('mapArea').innerHTML = urlStr;
                console.log(foundPath)
                document.getElementById('foundPath').innerHTML = data['foundPath'];
            }
        });
    });

    function drawUnescoSites(unesco_sites)
    {

        htmlString = '';
        $.each(unesco_sites, function( index, value ) {
            htmlString += '<li class="list-group-item">' + index + '<span class="activecase" style="float:right;"> AVG CASES-&nbsp;&nbsp;'+ value +'</span></li>';
          });
        document.getElementById('unesco_sites_list').innerHTML = htmlString;
        return htmlString; 
    }

    function drawPopularDest(popular_dest)
    {
        htmlString = '';
        $.each(popular_dest, function( index, value ) {
            htmlString += '<li class="list-group-item">' + index + '<span class="activecase" style="float:right;"> AVG CASES-&nbsp;&nbsp;'+ value +'</span></li>';
          });
        document.getElementById('pdest_list').innerHTML = htmlString;
        return htmlString; 
    }

    function drawSafeStates(safe_states)
    {
        htmlString = '';
        $.each(safe_states, function( index, value ) {
            htmlString += '<li class="list-group-item">' + index + '<span class="activecase" style="float:right;"> AVG CASES-&nbsp;&nbsp;'+ value +'</span></li>';
          });
        document.getElementById('safe_state_list').innerHTML = htmlString;
        return htmlString; 
    }

    function drawNewsFeed(newsFeed)
    {
        var feedString = '';
        $.each(newsFeed, function(key, value) {
            feedString +='<img src="static/icon/logo.png"></img>&nbsp;&nbsp;'
            feedString += '<span style="color:red;">' + key + '</span> : <span>' + value + '</span>&nbsp;&nbsp;&nbsp;&nbsp;';
        }); 
        document.getElementById('news').innerHTML = feedString;
    }
    var pList;
    function drawPage(data)
    {
        pList = data['cityList'];
        srcCity.value = 'Panipat , Haryana';
        destCity.value = 'Udaipur , Rajasthan';
        drawUnescoSites(data['unesco']);
        drawPopularDest(data['popular_dest']);
        drawSafeStates(data['safe_states']);
        drawNewsFeed(data['newsFeed']);
        $('#form1submit').click();

    }



    function foundPlace(obj,abc)
    {
        var id = $(abc).attr('id');
        $('#'+id).val($(obj).text());
        $('#'+ id +'_placeListSuggetion').fadeOut();
    }

    function matchedList(place, id)
    {
        htmlString = '<ul class="placeSuggestion" style="background-color:#00d4d4; position:absolute; width:300px;list-style-type:none;margin-left:0;">';
        $.each(pList, function( index, value ) {
            place = place.toUpperCase();
            value1 = value.toUpperCase();            
            if(value1.startsWith(place))
            {
            htmlString += '<li onclick="foundPlace(this, '+ id+')">' + value + '</li>';
            }
          });

        htmlString += '</ul>';
        return htmlString; 
    }

    $('.placeList').keyup(function(){
            var place = $(this).val();
            var id = $(this).attr('id')
            if(place != '')
            {
                $('#'+ id +'_placeListSuggetion').fadeIn();
                $('#'+ id +'_placeListSuggetion').html(matchedList(place, id));
            }
            else
            {
                $('#'+ id +'_placeListSuggetion').fadeOut();
                $('#'+ id +'_placeListSuggetion').html("");
            }
    });

    $('#loginSubmit').click(function(event){
        event.preventDefault();
        console.log("hello")
        var fd = new FormData();
        var uname = (document.getElementsByName("uname")[0]).value;
        var psw = (document.getElementsByName("psw")[0]).value;
        console.log(uname, " ", psw)
        fd.append("uname", uname)
        fd.append("psw", psw)
        
        $.ajax({
            url: '/login',
            data: fd,
            contentType: false,
            processData: false,
            type: 'POST',
            success: function(data){
                if(data['status'] == 'fail')
                {
                    document.getElementById('loginFailed').innerHTML = data['msg'];
                }
                else
                {
                    window.location.href = "admin";
                }
            }
        });

    });

// });



