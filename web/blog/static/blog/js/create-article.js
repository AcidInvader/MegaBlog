// const { data } = require("jquery");

console.log('create-article')
$(function () {
  $('#ArticleCreateForm').submit(createArticle);
});

function createArticle(e) {
    let form = $(this);
    e.preventDefault();
    console.log("start api request")
    let id = $(".user_id").text()
    let data = {
        title: this.title.value,
        category: this.category.value,
        author: {id},
        content: $(".note-editable").text(),
        slug: $(".note-editable").text().slice(0,200)
    };
    console.log('data', data)
    $.ajax({
        url: "/api/v1/article/blog/create-article/",
        type: "POST",
        dataType: "json",
        data: data,
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