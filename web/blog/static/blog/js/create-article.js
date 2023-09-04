console.log('create-article')
$(function () {
  $('#ArticleCreateForm').submit(createArticle);
});

function createArticle(e) {
    e.preventDefault();
    let form = $(this);
    console.log("start api request...", form)
    let formData = new FormData(this);
    formData.append("content", $(".note-editable").text());
    // for (let item of formData) {
    //     console.log(item[0], item[1])
    // };

    $.ajax({
        url: "/api/v1/article/blog/create-article/",
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        success: successHandler,
        error: errorHandler
    })
};

function successHandler(data) {
    console.log("success", data)
};

function errorHandler(data) {
    console.log("error", data)
};