function validateToken()
{
    var access_token = window.localStorage.getItem("access_token");
    if(access_token==null)
        window.location.pathname = '/app/login';
    else{
        $.ajax({
            url: "/app/validateToken/",
            type: "POST",
            data: {
                "csrfmiddlewaretoken" : "{{ csrf_token }}",
                "access_token":access_token,
            },
            success: function(response) {
                
            },
            error: function(xhr, a, b)
            {
                window.location.pathname = '/app/login';
            }
        });
    }       
}
window.onpaint = validateToken();