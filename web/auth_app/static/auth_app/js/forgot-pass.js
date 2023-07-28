console.log('forgot-pass')
$(function () {
    $('#forgotPasswordForm').submit(forgotPassword);
});

function forgotPassword(e) {
    let form = $(this);
    e.preventDefault();
    console.log('forgot-password')
    $.ajax({
        url: "/api/v1/auth/password/reset/",
        type: "POST",
        dataType: "json",
        data: form.serialize(),
        success: successHandler,
        error: erroeHandler
    })
}

function successHandler(data) {
    console.log("success", data)
    $('#mail-sent').html('Link has sent to you email box. Please check the box.').fadeIn();
    setTimeout(() => {
        location.href='/';
    }, 2000);
}

function erroeHandler(data) {
    console.log('error handler...', data);
    let response = String(Object.values(data.responseJSON))
    $('#mail-sent').html(response).fadeIn();
    console.log('error handled')
}