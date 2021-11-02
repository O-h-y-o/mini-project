$('#login').click(function() {
    let id = $('#id>input').val();
    let pw = $('#pw>input').val();

    $.ajax({
        type: "POST",
        url: "/logins",
        data: {
            id_give: id, pw_give: pw
        },
        success: function (response) {
            if (response['result'] == 'success') {
                $.cookie('mytoken', response['token'], {path: '/login_main'});
                window.location.replace("/login_main")
            } else {
                alert(response['msg'])
            }
        }
    })
})