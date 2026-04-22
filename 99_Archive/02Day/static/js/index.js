function postLoad(){
fetch('/api/board')
.then(res => res.json())
.then(data => {
    const posts = data;
    let html = "";
    for(let i = 0; i<posts.length; i++){
        html +=`<b><a href="/detail/${posts[i].id}">${posts[i].title}</a></b> <small>${posts[i].nickname}</small><hr>`
    }
    document.getElementById("post_list").innerHTML = posts;
})
.catch(error => {
    console.error(error)
})
}