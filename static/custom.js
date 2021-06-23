function student_list() {
    window.location.href = '/student/'
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
      message: " Do you really want to delete?",
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
                url: '/student/' + student_id,
                type: 'DELETE',
                success: function (result) {
                  toastr.success("deleted successfully");
                  setTimeout(window.location.reload(), 60000)
                },
                error: function (response) {
                  toastr.error("Not deleted ")
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
    var student_obj = { student_name: student_name, student_age: student_age };
    var student = JSON.stringify(student_obj);
    $.ajax({
        url: '/student/' + student,
        type: 'POST',
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
    var obj = { student_name: student_name, student_age: student_age, student_id: student_id };
    var json = JSON.stringify(obj);
    console.log(json);
    $.ajax({
        url: '/student/' + json,
        type: 'PUT',
        success: function (response) {
            toastr.success("Data updated successfully");
            window.location.href = '/student/'
            
        },
        error: function (error) {
            toastr.error("data updation failed");
        }
    });
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
        document.getElementById("message-form").innerHTML="confirm password does not match with above password";
        return false
    }
    if((email.match('[^@]+@[^@]+\.[^@]+'))){               
        return true;
    }else{
        document.getElementById("email_id").style.borderColor="red";
        document.getElementById("message-form").innerHTML="invalid Email";
        return false
    }
}

function signup(){
    window.location.href="/auth/signup/";
}

function create_user_role(){
  var username = document.getElementById("username").value;
  var role = $('#select').val().join(',');
  var new_role = { username: username, role: role };
  
  var new_role_1 = JSON.stringify(new_role);
  console.log(new_role_1);
  
  $.ajax({
  url: '/admin/create_role/' + new_role_1,
  type: 'POST',
  success: function (response) {
      response=JSON.parse(response);
      console.log(response);
      if(response.status==false){

          toastr.error(response.error);
          
      }else{
          window.location.href="/admin/";
      }
      
      
      /*window.location.href="/admin/";*/
  },
  error: function (error) {
      console.log(error);
      
  }
});
}

function edit_role(user_id){
  window.location.href="/admin/user_role_form/?user_id="+user_id;
}