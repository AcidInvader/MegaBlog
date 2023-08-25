console.log('category-list')
$(function () {
  $(document).ready(articleList);
});

function articleList(e) {
    console.log('articleList works...')
    $.ajax({
        url: "/api/v1/article/blog/category-list",
        type: "GET",
        dataType: "json",
        success: successHandler,
        error: errorHandler
    })
}

function successHandler(data) {
    console.log('success...', data)
    data.forEach(element => {
      console.log(element['name']);
    });
}

function errorHandler(data) {
    console.log('error...', data)
}


