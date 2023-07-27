
$.ajax({
    url: "/api/v1/auth/sign-up/verify/",
    type: "POST",
    dataType: "json",
    data: getQueryParams(),
    success: successHandler,
    error: errorHandler
})


function successHandler(data) {
    console.log("success", data);
    $('h2').html('Congratulations! Your email is verified!')
    $('.js-verified').fadeIn(); // make the css property visible
    setTimeout(() => {
        location.href='/login/';
    }, 3000);
    
}

function errorHandler(data) {
    console.log("error", data);
    $('h2').html('We are sorry, your email is not verified.')
    $('.js-verified').fadeIn();
    setTimeout(() => {
        location.href='/register/'; 
    }, 3000);
}
