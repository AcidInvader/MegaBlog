$(function () {
    $.ajax({
        url: "/api/v1/article/blog/",
    }).then(function (data) {
        successHandler(data)
    })
});