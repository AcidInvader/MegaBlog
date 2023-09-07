console.log('comment-creating...')
console.log("article_id", window.article_id);

$(function() {
    $('#comment-form').submit(createComment)
});

function createComment(e) {
    e.preventDefault();
    console.log('start creating comment...');
    let data = {
        content: $("#content-comment").val(),
        article: article_id,
    }

    $.ajax({
        url: "/api/v1/article/blog/create-comment/",
        type: "POST",
        data: data,
        success: successHandler,
        error: errorHandler
    })
};

function successHandler(data) {
    console.log("success", data)
}

function errorHandler(data) {
    console.log("error", data)
}