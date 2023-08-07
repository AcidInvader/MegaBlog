$(function () {
    const getParams = getQueryParams()
    let id = getParams.id
    $.ajax({
        url: `/api/v1/article/blog/${id}`,
    }).then(function (data) {
        console.log(data)
        successHandler(data)
    })

});

function successHandler(data) {
    $('h1').html(data.title);
    $('.fa-user').html(data.author.full_name);
    $('.fa-calendar').html(data.updated);
    // $('.img-responsive').attr('src', `${data.image}`);
    $('#content').html(data.content);
    
};
console.log('blog-detail')
