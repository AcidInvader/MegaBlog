console.log("reset Hello")

$(function () {
    $('#resetPasswordForm').submit(resetPassword);
});

function resetPassword(e) {
    let form = $(this);
    e.preventDefault(); // this method stop form request
    const getParams = getQueryParams()
    let data = {
        password_1: this.password_1.value,
        password_2: this.password_2.value,
        uid: getParams.uid,
        token: getParams.token,
    };
    
    $.ajax({
        url: "/api/v1/auth/password/reset/confirm/",
        type: "POST",
        dataType: "json",
        data: data,
        success: successHandler,
        error: errorHandler
    })
}

function successHandler(data) {
    console.log("success", data);
}

function errorHandler(data) {
    console.log("error", data);
    let response = String(Object.values(data.responseJSON));
    $('#service-message').html(response).fadeIn();
    console.log('error handled')
}