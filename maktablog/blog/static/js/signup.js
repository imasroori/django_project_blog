
    $("#id_username").change(function () {
        var username = $(this).val();
      $.ajax({
      url:'/ajax/validate_username',
      data:{
      'username': username
      },
      datatype:'json',
      success: function(data){
      if (data.is_taken){
                alert("کاربری با این نام کاربری موجود است، لطفا یک نام کاربری دیگری انتخاب کنید")
                }
        }

      })
    });




