$(function () {
  // $(document).on("click", "a.login", login);
  $('#loginForm').submit(login);
});

function login(e) {
  let form = $(this);
  e.preventDefault();
  $.ajax({
    url: form.attr("action"),
    type: "POST",
    dataType: 'json',
    data: form.serialize(),
    success: function (data) {
      console.log(data)
      location.reload();
    },
    error: function (data) {
      $("#emailGroup").addClass("has-error");
      $("#passwordGroup").addClass("has-error");
      $("#passwordGroup").append(
        '<div class="help-block">' + data.responseJSON.email + "</div>"
      );

    }
  })
}
