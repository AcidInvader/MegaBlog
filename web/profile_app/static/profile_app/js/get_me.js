$(function () {
    console.log("page construction has started...")
    $.ajax({
        url: "/api/v1/profiles/me/",
    }).then(function (data) {
        successHandler(data)
    })
});

function successHandler(data) {
    console.log("get request has sent ->>>", data)
    $("h1").html(data.full_name);
    $(".posts").html(data.article_count);
    $("#firstname").attr("placeholder", data.first_name);
    $("#lastname").attr("placeholder", data.last_name);
    $("#email").attr("placeholder", data.email);
    $("#avatar").attr("src", data.avatar);
}