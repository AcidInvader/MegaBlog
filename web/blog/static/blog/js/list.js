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
        conteiner.appendChild(article);
    });
    
}

console.log('blog-list')
