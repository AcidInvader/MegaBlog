console.log('category-list')
$(function () {
  categoryList();
});

function categoryList() {
    console.log('articleList works...')
    $.ajax({
        url: "/api/v1/article/blog/category-list",
        type: "GET",
        dataType: "json",
        success: successHandler,
        error: errorHandler,
    })
}

function successHandler(data) {
    console.log('success...', data)
    let conteiner = document.getElementById("category");
    if (Array.isArray(data)) {
      data.forEach(element => {
        console.log(element['name']);
        let category =  element['name']
        let category_item = document.querySelector("#drop_item").cloneNode(true);
        category_item.value = element['id']
        category_item.innerHTML = `${category}`;
        conteiner.appendChild(category_item);
      });
    } else {
      console.log('error', data)
      $('#service-message').html('Congratulations, you have created an Article! You will see the article after success moderation by service.').fadeIn();
    setTimeout(() => {
        location.href='/';
    }, 3000);
    }
}

function errorHandler(data) {
    console.log('error...', data)
}


