function postLoad(){
fetch('/api/board')
.then(res => res.json())
.then(data => {
    const posts = data.posts;
    let html = "";
    for(let i = 0; i<posts.length; i++){
        html +=`<b><a href="/detail/${posts[i].id}">${posts[i].title}</a></b> <small>${posts[i].nickname}</small><hr>`
    }
    document.getElementById("message").innerText = data.nickname;
    document.getElementById("post_list").innerHTML = html;
})
.catch(error => {
    console.error(error)
})
}
postLoad();