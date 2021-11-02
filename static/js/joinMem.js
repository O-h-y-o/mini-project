$('#join').click(function() {
    let id = $('#id>input').val();
    let pw = $('#pw>input').val();

    $.ajax({
        type: "POST",
        url: "/join_info",
        data: {
            id_give: id, pw_give: pw
        },
        success: function (response) {
            alert(response["msg"]);
        }
    })
});