$(function () {
    $.ajax({
        url: "/api/v1/article/blog/",
    }).then(function (data) {
        successHandler(data)
    })
});

function successHandler(data) {
    console.log("it's working", data);
    let conteiner = document.getElementById("container");
    data.results.forEach(function(element) {
        let article = document.querySelector(".post").cloneNode(true);
        article.removeAttribute("style");
        article.querySelector(".post-title").innerHTML = `${element.title}`;
        article.querySelector("#Author_name").innerHTML = `${element.author.full_name}`;
        article.querySelector(".col-md-9").innerHTML = `${element.slug}`;
        article.querySelector(".btn-read-more").id = `${element.id}`;
        conteiner.appendChild(article);
    });
    
}

console.log('blog-list')

$(document).on('click', '.btn', function(e) {
    e.preventDefault();
    let article_id = e.target.id
    location.href = `/blog/article?id=${article_id}`
    
});

$(document).on('click', '.col-md-9', function(e) {
    e.preventDefault();
    console.log(e);
    let article_slug = e.target.childNodes[0].data
    location.href = `/blog/article?id=${article_slug}`
});





