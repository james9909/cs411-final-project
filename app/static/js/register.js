$("#register-form").submit(function(e) {
    e.preventDefault();
    $("#register-submit").attr("disabled", "disabled");
    apiCall("POST", "/api/user/register", {
        username: $("#username").val(),
        password: $("#password").val(),
        re_password: $("#re_password").val()
    },
        function(response) {
            $("#register-submit").removeAttr("disabled", "disabled");
            window.location = "/login";
        },
        function(response) {
            $("#register-submit").removeAttr("disabled", "disabled");
        }
    );
})
