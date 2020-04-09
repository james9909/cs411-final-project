$("#login-form").submit(function(e) {
    e.preventDefault();
    $("#login-submit").attr("disabled", "disabled");
    apiCall("POST", "/api/user/login", {
        username: $("#username").val(),
        password: $("#password").val()
    },
        function(response) {
            $("#login-submit").removeAttr("disabled", "disabled");
            window.location = "/";
        },
        function(response) {
            $("#login-submit").removeAttr("disabled", "disabled");
        }
    );
})
