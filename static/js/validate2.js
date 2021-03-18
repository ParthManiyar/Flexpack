function validateToken()
{
    var access_token = window.localStorage.getItem("access_token");
    if(access_token==null){
        $("#logout").css("display", "none");
        $("#saved_design").css("display", "none");
    }
    else{
        $.ajax({
            url: "/app/validateToken/",
            type: "POST",
            data: {
                "csrfmiddlewaretoken" : "{{ csrf_token }}",
                "access_token":access_token,
            },
            success: function(response) {
                $("#login").css("display", "none");
                $("#signup").css("display", "none");
            },
            error: function(xhr, a, b)
            {
                $("#logout").css("display", "none");
                $("#saved_design").css("display", "none");
            }
        });
    }       
}
window.onload = validateToken();