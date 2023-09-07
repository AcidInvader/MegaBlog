// this function gets the data for show them on the page 
$(function () {
    const getParams = getQueryParams()
    let article_id = getParams.id
    console.log('article_id...', article_id);
    $.ajax({
        url: `/api/v1/article/blog/${article_id}`,
    }).then(function (data) {
        successHandler(data)
    })

});

function successHandler(data) {
    console.log('article_detail...', data)
    $('h1').html(data.title);
    $('.fa-user').html(data.author.full_name);
    $('.fa-calendar').html(data.updated);
    $('.img-responsive').attr('src', `${data.image}`);
    $('#content').html(data.content);
    // take the list of comments and load on the page in the loop
    commentList();
    
};
console.log('blog-detail')

$(function() {
    $("#comment-form").submit(createComment);
});

// this finction creating a first comment
function createComment(e) {
    e.preventDefault();
    const getParams = getQueryParams()
    let article_id = getParams.id
    console.log("create-comment...");
    let comment_data = {
        content: $("#content-comment").val(),
        article: article_id,
    };

    $.ajax({
        url: "/api/v1/article/blog/create-comment/",
        type: "POST",
        data: comment_data,
        dataType: "JSON",
        success: successCommentHandler,
        error: errorCommentHandler,
    })
}

function successCommentHandler(comment_data) {
    console.log("everything is OK...", comment_data)
};

function errorCommentHandler(comment_data) {
    console.log("everything is OK...", comment_data)
};

// this function gets the list of data comments and shows it on the page
function commentList() {
    const getParams = getQueryParams()
    let article_id = getParams.id
    $.ajax({
        url: `/api/v1/article/blog/comment-list/${article_id}`,
        type: "GET",
        dataType: "json",
        success: successCommentListHandler,
        error: errorCommentListHandler
    })
}

function successCommentListHandler(data) {
    let conteiner = document.getElementById("container");
    data['results'].forEach(function(comment) {
        console.log('comment...', comment);
        var comment_field = document.querySelector("#comment").cloneNode(true);
        console.log("comment_field", comment_field);
        var user = comment_field.querySelector("#user");
        var created_at = comment_field.querySelector("#created-at");
        var content = comment_field.querySelector("#comment-content");
        user.textContent = comment.user['full_name'];
        created_at.innerHTML = comment.created;
        content.textContent = comment.content;
        conteiner.appendChild(comment_field);
    });
}

function errorCommentListHandler(data) {
    console.log('error', data);
    
}
