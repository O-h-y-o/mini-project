$('.review_button').click(function () {
    $('.review').toggleClass('hide-out');
    // $('#reviewMemo').toggleClass('show');
    // $('#reviewTitle').toggleClass('show');
});


$('.upload_review').click(function () {
    let url = $('#reviewURL').val()
    let reviewMemo = $('#reviewMemo').val()
    let reviewTitle = $('#reviewTitle').val()
    $.ajax({
        type: "POST",
        url: "/viewList",
        data: {url_give: url, reviewMemo_give: reviewMemo, reviewTitle_give: reviewTitle},
        success: function (response) {
            alert(response["msg"]);
            window.location.reload();
        }
    })
})


$('.userSelect').click(function () {
    $('#userSelect_click').toggleClass('hide-out');
})

$('.select_close').click(function () {
    $('#userSelect_click').removeClass('hide-out');
})