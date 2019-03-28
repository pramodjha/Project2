
$("#id_teamfilter").change(function () {
    var team_id = $(this).val();  // get the selected country ID from the HTML input
   console.log(team_id)
   $.ajax({
     url: "{% url 'ajax_load_mimember' %}",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
     data: {
       'team_id': team_id     // add the country id to the GET parameters
     },
       success: function (data) {   // `data` is the return of the `load_cities` view function
       $("#id_memberfilter").html(data);  // replace the contents of the city input with the data that came from the server
     }
   });
 });

   $("#id_memberfilter").focus(function () {
      var team_id = $("#id_teamfilter").val();  // get the selected country ID from the HTML input
      var member_id = $("#id_memberfilter").val();  // get the selected country ID from the HTML input
     console.log(team_id)
     console.log(member_id)
     $.ajax({
       url: "{% url 'ajax_load_mimember' %}",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
       data: {
         'team_id': team_id,
         'member_id': member_id     // add the country id to the GET parameters
       },
         success: function (data) {
         $("#id_memberfilter").html(data);  // replace the contents of the city input with the data that came from the server
       }
     });
   });


 $(".btn-default").click(function () {
      var url = $("#extractdata").attr("data-mimember-url");
      var team_id = document.getElementById("id_teamfilter").value;
      console.log(team_id)
      $.ajax({
        url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'team_id': team_id,
        },
          success: function (data) {
          $("#id_memberfilter").html(data);
            // replace the contents of the city input with the data that came from the server
        }
      });

  });



  $('#modal').submit( function(event) {
      // disable to avoid double submission
      $('#submit_button').attr('disabled', true);
  });


  $("#id_username").keyup(function () {
     var url = $("#signupform").attr("data-signup-url");  // get the url of the `load_cities` view
     var username = $(this).val();  // get the selected country ID from the HTML input
     console.log(username)
     $.ajax({                       // initialize an AJAX request
       url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
       data: {
         'username': username     // add the country id to the GET parameters
       },
         success: function (data) {   // `data` is the return of the `load_cities` view function
         $("#usercheck").html(data);  // replace the contents of the city input with the data that came from the server
       }
     });
   });


   $("#id_email").keyup(function () {
      var url = $("#signupform").attr("data-signup-url");  // get the url of the `load_cities` view
      var emailid = $(this).val();  // get the selected country ID from the HTML input
      console.log(emailid)
      $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'emailid': emailid     // add the country id to the GET parameters
        },
          success: function (data) {   // `data` is the return of the `load_cities` view function
          $("#emailcheck").html(data);  // replace the contents of the city input with the data that came from the server
        }
      });
    });

    $("#id_passwordagain").keyup(function () {
       var url = $("#signupform").attr("data-signup-url");  // get the url of the `load_cities` view
       var passwordagain = $(this).val();  // get the selected country ID from the HTML input
       var password = document.getElementById("id_password").value;
       console.log(passwordagain)
       console.log(password)
       $.ajax({                       // initialize an AJAX request
         url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
         data: {
           'passwordagain': passwordagain , 'password': password   // add the country id to the GET parameters
         },
           success: function (data) {   // `data` is the return of the `load_cities` view function
           $("#passwordcheck").html(data);  // replace the contents of the city input with the data that came from the server
         }
       });
     });

     $("#id_passwordagain").keyup(function () {
        var url = $("#signupform").attr("data-signup-url");  // get the url of the `load_cities` view
        var passwordagain = $(this).val();  // get the selected country ID from the HTML input
        var password = document.getElementById("id_password").value;
        console.log(passwordagain)
        console.log(password)
        $.ajax({                       // initialize an AJAX request
          url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
          data: {
            'passwordagain': passwordagain , 'password': password   // add the country id to the GET parameters
          },
            success: function (data) {   // `data` is the return of the `load_cities` view function
            $("#passwordcheck").html(data);  // replace the contents of the city input with the data that came from the server
          }
        });
      });



      $("#id_teamfilter").change(function () {
          var team_id = $(this).val();  // get the selected country ID from the HTML input
         console.log(team_id)
         $.ajax({
           url: "{% url 'ajax_load_mimember' %}",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
           data: {
             'team_id': team_id     // add the country id to the GET parameters
           },
             success: function (data) {   // `data` is the return of the `load_cities` view function
             $("#id_memberfilter").html(data);  // replace the contents of the city input with the data that came from the server
           }
         });
       });

         $("#id_memberfilter").focus(function () {
            var team_id = $("#id_teamfilter").val();  // get the selected country ID from the HTML input
            var member_id = $("#id_memberfilter").val();  // get the selected country ID from the HTML input
           console.log(team_id)
           console.log(member_id)
           $.ajax({
             url: "{% url 'ajax_load_mimember' %}",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
             data: {
               'team_id': team_id,
               'member_id': member_id     // add the country id to the GET parameters
             },
               success: function (data) {
               $("#id_memberfilter").html(data);  // replace the contents of the city input with the data that came from the server
             }
           });
         });


       $(".btn-default").click(function () {
            var url = $("#extractdata").attr("data-mimember-url");
            var team_id = document.getElementById("id_teamfilter").value;
            console.log(team_id)
            $.ajax({
              url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
              data: {
                'team_id': team_id,
              },
                success: function (data) {
                $("#id_memberfilter").html(data);
                  // replace the contents of the city input with the data that came from the server
              }
            });

        });


/// feedback question:
$(document).ready(function() {
    $('#example').DataTable(
    {
      fixedHeader: true,
    });
});

/// Internal_Task_Choice_View
$(document).ready(function() {
    $('#example1').DataTable(
    {
      fixedHeader: true,
      scrollY: '90vh',
      scrollCollapse: true,
      scrollX: true,
      columnDefs: [
            { width: 400, targets: 0 }
        ],

    });

} );
