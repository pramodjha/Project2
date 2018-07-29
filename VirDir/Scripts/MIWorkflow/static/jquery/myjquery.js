
$("#setdate").click(function () {
    var datevalue = $("#id_trackingdatetime").val() // get the selected country ID from the HTML input
    console.log(datevalue)
    $.ajax({
       type: "GET",
        url: "{% url 'sdate' %}",
        data: {'dv': datevalue},

        success: function (data) {   // `data` is the return of the `load_cities` view function
        $("#table2").html(data);  // replace the contents of the city input with the data that came from the server
      },
        error: function(request,status,errorThrown) {
       // There's been an error, do something with it!
       // Only use status and errorThrown.
       // Chances are request will not have anything in it.
     }

          });

          });


  $(document).ready(function() {
      $('#example').DataTable(
      {
        fixedHeader: true,
        scrollY: '90vh',
        scrollCollapse: true

      });

  } );


// $("#id_trackingdatetime").change(function () {
  //  var url = $("#datatable").attr("ajax_load_datevalues");  // get the url of the `load_cities` view
  //  var datevalue = $(this).val();  // get the selected country ID from the HTML input
    //console.log(datevalue)
    //$.ajax({                       // initialize an AJAX request
    //  url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
      //data: {
      //  'dv': datevalue     // add the country id to the GET parameters
      //}
        //success: function (data) {   // `data` is the return of the `load_cities` view function
        //$("#datatable").html(data);  // replace the contents of the city input with the data that came from the server

  //  });
//  });


//$("#id_trackingdatetime").change(function () {
//   var datevalue = $(this).val();
//   console.log(datevalue)  // get the selected country ID from the HTML input
//        $.ajax({
//            type: "GET",
//            url: "{% url 'ajax_load_datavalues' %}",  // URL to your view that serves new info
//            data: {'dv': datevalue}
//        })
//        .done(function(response) {
//           $('#table2').html(response);

  //      });
  //  });


//    $("#id_trackingdatetime").change(function () {
//       var datevalue = $(this).val();
//       console.log(datevalue)  // get the selected country ID from the HTML input
//            $.ajax({
//                type: "GET",
//                url: "{% url 'sdate' %}",  // URL to your view that serves new info
//                data: {'dv': datevalue}
//            })
//            .done(function(response) {
//               $('#table2').html(response);

  //          });
  //      });



 function getTimeStamp() {
        var now = new Date();
        return ((now.getMonth() + 1) + '/' + (now.getDate()) + '/' + now.getFullYear() + " " + now.getHours() + ':'
  + ((now.getMinutes() < 10) ? ("0" + now.getMinutes()) : (now.getMinutes())) + ':' + ((now.getSeconds() < 10) ? ("0" + now.getSeconds()) : (now.getSeconds())));
 }

 function setstartTime() {
  var buttcaption = document.getElementById("1");
   if (buttcaption.innerHTML=="Start")
  {buttcaption.innerHTML ="Stop";
  document.getElementById('id_startdatetime').value = getTimeStamp();
}
else if (buttcaption.innerHTML=="Stop")
{buttcaption.innerHTML ="Start";
   document.getElementById('id_stopdatetime').value = getTimeStamp();}
 }
