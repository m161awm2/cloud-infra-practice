document.getElementById("form").addEventListener("submit",function(e){
e.preventDefault();
const title = document.getElementById("title").value;
const content = document.getElementById("content").value;

if(title.trim() === "" || content.trim() === ""){
    document.getElementById("message").innerText = "빈 문자열을 넣지마세요!";
}
fetch("/api/write",{
    method:"POST",
    headers:{
        "Content-Type" : "application/json"
    },
    body:JSON.stringify({
        title,
        content
    })
})
.then(res=>res.json())
.then(data=>{
    alert(data.message);
})
.catch(error=>{
    console.error(error);
})
})