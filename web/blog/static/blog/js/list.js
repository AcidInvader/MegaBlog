$(function () {
    $.ajax({
        url: "/blog/"
    }).then(function (result) {
        result.serialize()
        console.log("result", result)
    })
});

console.log('blog-list')
