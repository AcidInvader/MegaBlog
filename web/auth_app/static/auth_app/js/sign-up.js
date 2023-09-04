console.log('sing-up')
$(function () {
  $('#signUpForm').submit(singUp);
});

function singUp(e) {
  let form = $(this);
  e.preventDefault();
  console.log('here')
  $.ajax({
    url: "/api/v1/auth/sign-up/",
    type: "POST",
    dataType: "json",
    data: form.serialize(),
    success: succesHandler,
    error: errorHandler
  })
}

function succesHandler(data) {
  console.log("succsess", data);
  $('#service-message').html('Wehave sent a mail to you. Please check the box.').fadeIn();
  setTimeout(() => {
    location.href='/';
}, 3000);
}

function errorHandler(data) {
  console.log("error", data);
  let response = String(Object.values(data.responseJSON));
  $('#service-message').html(response).fadeIn();
  console.log(response);
  }

