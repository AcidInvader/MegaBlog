// this function gets the data for show them on the page 
$(function () {
    const getParams = getQueryParams();
    let article_id = getParams.id;
    console.log('article_id...', article_id);
    $.ajax({
        url: `/api/v1/article/blog/${article_id}`,
    }).then(function (data) {
        successHandler(data);
    });

});

function successHandler(data) {
    console.log('article_detail...', data);
    $('h1').html(data.title);
    $('.fa-user').html(data.author.full_name);
    $('.fa-calendar').html(data.updated);
    $('.img-responsive').attr('src', `${data.image}`);
    $('#content').html(data.content);
    commentList();
    
};

$(function() {
    $("#comment-form").submit(createComment);
});

// this finction creating a main comment
function createComment(e) {
    e.preventDefault();
    const getParams = getQueryParams();
    let article_id = getParams.id;
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
    console.log("everything is OK...", comment_data);
};

function errorCommentHandler(comment_data) {
    console.log("everything is OK...", comment_data);
};

// this function gets the list of data comments and shows it on the page
function commentList() {
    const getParams = getQueryParams();
    let article_id = getParams.id;
    $.ajax({
        url: `/api/v1/article/blog/comment-list/${article_id}`,
        type: "GET",
        dataType: "json",
        success: successCommentListHandler,
        error: errorCommentListHandler
    });
};

// this function show comments on the page
function successCommentListHandler(data) {
    let conteiner = document.getElementById("container");
    data['results'].forEach(function(comment) {
        console.log('comment...', comment);
        var comment_field = document.querySelector(".comment").cloneNode(true); 
        comment_field.querySelector("#user").innerHTML = `${comment.user['full_name']}`;
        comment_field.querySelector("#created-at").innerHTML = `${comment.created}`;
        comment_field.querySelector("#comment-content").innerHTML = `${comment.content}`;
        comment_field.querySelector(".chi-comm-button").setAttribute('id', comment.id);
        comment_field.querySelector(".form-child-comment").setAttribute('id', "form_" + comment.id);
        conteiner.appendChild(comment_field);
        if (comment.children.length > 0) {
            comment.children.forEach(function(child) {
                console.log("child...", child);
                let childComment = document.querySelector(".child-comment").cloneNode(true);
                childComment.querySelector("#user").innerHTML = `${child.user}`;
                childComment.querySelector("#created-at").innerHTML = `${child.created}`;
                childComment.querySelector("#comment-content").innerHTML = `${child.content}`;
                conteiner.appendChild(childComment);
            })
            // here the logick of add child comment under this comment
        }
    });
  
    // this finction responseble for show child comment field 
    conteiner.addEventListener('click', function(event){
        let target = event.target;
        let answer_form = document.getElementById("form_" + target.id);
        if(answer_form.style.display === 'none') {
            answer_form.style.display = 'block'; 
        } else {
            answer_form.style.display = 'none';
        };
    });
    var forms = document.querySelectorAll(".form-child-comment");

    // add eventLostener of "submit" for each form
    forms.forEach(function(form) {
        form.addEventListener("submit", function(event) {
            event.preventDefault();
            // get the link of event
            var submittedForm = event.target;
            createChildComment(submittedForm);
        });
    });

};

function errorCommentListHandler() {
    console.log("error...", data);
};

// This function create child comment
function createChildComment(form) {
    var form_field = form.querySelector(".chi-comm-field");
    var content = form_field.value;
    var form_id = (form.id).split("_");
    var parent = form_id[1];
    const getParams = getQueryParams();
    let article_id = getParams.id;

    var data = {
    content: content,
    parent: parent,
    article: article_id
    };

    $.ajax({
        url: "/api/v1/article/blog/create-comment/",
        type: "POST",
        dataType: "JSON",
        data: data,
        success: successChildCommentCreate,
        error: errorChildCommentCreate
    });
};

function successChildCommentCreate(data) {
    console.log("success_child_create", data)
};

function errorChildCommentCreate(data) {
    console.log("error_child_create", data)
};