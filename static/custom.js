window.dataLayer = window.dataLayer || [];
function student_list() {
  window.location.href = '/student/' ; 
  // window.dataLayer.push({
  //   "test_var":"button"
  //   });
   

}

function student_form() {
    window.location.href = '/student/studentForm/';
}
function show_alert_user(){
 toastr.warning("could'nt use this option because you don't have access");
}
function go_to_AdminPanel() {
    window.location.href = '/admin/';
}
function create_user_role_form() {
    window.location.href = '/admin/user_role_form/';
}

function update_form(id) {

    var id = Number(id);
    window.location.href = '/student/studentForm/?id=' + id;
}
 
function go_to_homepage() {
  window.location.href = '/'
}

function logout() {
  // console.log(hello);
    bootbox.confirm({
      message: " Do you really want to Logout ?",
      buttons: {
        confirm: {
          label: 'Yes',
          className: 'btn-success'
        },
        cancel: {
          label: 'No',
          className: 'btn-danger'
        }
      },
      callback: function (result) {
        if (result) {
          window.location.href = '/auth/logout/';
          toastr.success("Logged out successfully")
        }
      }
    });
}
$(document).ready(function () {
    $('#example').DataTable();
    $('select').selectpicker();
  });

function delete_student(student_id) {
    bootbox.confirm({
      message: " Do you really want to delete, delete cause the data to be permanently deleted?",
      buttons: {
        confirm: {
          label: 'Yes',
          className: 'btn-success'
        },
        cancel: {
          label: 'No',
          className: 'btn-danger'
        }
      },
      callback: function (result) {
        console.log(result)
        if (result) {
          $.ajax
            (
              {
                url: '/student/' ,
                type: 'DELETE',
                dataType: 'json',
                data:JSON.stringify({student_id : student_id}),
                success: function (result) {
                  toastr.success("deleted successfully");
                  setTimeout(window.location.reload(), 60000)
                },
                error: function (error) {
                  toastr.error(error)
                }
              }
            );
        }
      }
    });
};



function save_student() {
    var student_name = document.getElementById("name").value;
    var student_age = Number(document.getElementById("age").value);
    var student = { student_name: student_name, student_age: student_age };
    var student = JSON.stringify(student);
    console.log(student);
    $.ajax({
        url: '/student/' ,
        type: 'POST',
        dataType: 'json',
        data: student,

        success: function (response) {
            toastr.success("Data saves successfully")
            window.location.href = '/student/'
        },
        error: function (error) {
            toastr.error("data not saved");
        }
    });
}

function update_student(student_id) {
    
    var student_name = document.getElementById("name").value;
    var student_age = Number(document.getElementById("age").value);
    student_id = Number(student_id);
    if (student_age == 0) {
        student_age = Number("{{record['student_age'][0]}}");
    }
    if (student_name == "") {
        student_name = "{{record['student_name'][0]}}";
    }
    console.log(student_id);
    var student = { student_name: student_name, student_age: student_age, student_id: student_id };
    var student = JSON.stringify(student);
    bootbox.confirm({
      message: " Do you really want to update, ?",
      buttons: {
        confirm: {
          label: 'Yes',
          className: 'btn-success'
        },
        cancel: {
          label: 'No',
          className: 'btn-danger'
        }
      },
      callback: function (result) {
        console.log(result)
        if (result) {
          $.ajax({
            url: '/student/' ,
            type: 'PUT',
            dataType: 'json',
            data: student,
            success: function (response) {
                window.location.href = '/student/'
            },
            error: function (error) {
                toastr.error("data updation failed");
            }
        });
        }
      }
    });


    // $.ajax({
    //     url: '/student/' ,
    //     type: 'PUT',
    //     dataType: 'json',
    //     data: student,
    //     success: function (response) {
    //         window.location.href = '/student/'
    //     },
    //     error: function (error) {
    //         toastr.error("data updation failed");
    //     }
    // });
}

function validation(){
    var email=document.getElementById("email_id").value;
    var password=document.getElementById("password").value;
    var repassword=document.getElementById("re-password").value;
    var isvalid ;
    
    if(password==repassword){
        console.log(" pass word not match");
    }else{
        document.getElementById("password").style.borderColor="red";
        document.getElementById("re-password").style.borderColor="red";
        document.getElementById("sign-up-failed").innerHTML="confirm password does not match with above password";
        return false
    }
    if((email.match('[^@]+@[^@]+\.[^@]+'))){               
        return true;
    }else{
        document.getElementById("email_id").style.borderColor="red";
        document.getElementById("sign-up-failed").innerHTML="invalid Email";
        return false
    }
}

function signup(){
    window.location.href="/auth/signup/";
}

function create_user_role(){
  var username =$('#username').val();
  var roles = $('#select').val().join(',');
  var user_new_role = { username: username, roles: roles };
  
  var user_new_role = JSON.stringify(user_new_role);
  console.log(user_new_role);
  
  $.ajax({
  url: '/admin/create_role/',
  type: 'POST',
  dataType: 'json',
  data: user_new_role,
  success: function (response) {
      if(response.error==true){
        toastr.error(response.message);  
      }else{
        console.log("Status : ok");
        window.dataLayer.push({
          "event":"CreateUserRole",
          "Username": "{{user}}",
          "platform_dv":"web"
        });
        window.location.href="/admin/";
      }
  },
  error: function (error) {
      toastr.error(error);   
    }
 });
}

function edit_role(user_id){
  window.location.href="/admin/user_role_form/?user_id="+user_id;
}


function go_back(){
  history.back();
}