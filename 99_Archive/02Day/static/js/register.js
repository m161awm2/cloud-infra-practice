document.getElementById("form").addEventListener("submit",function(e){
    e.preventDefault();
    const nickname = document.getElementById("nickname").value;
    const password = document.getElementById("password").value;
    if(nickname.trim() === "" || password.trim() === ""){
    document.getElementById("message").innerText = "빈 값을 절대 넣지마세요";
    return;
    }
    fetch('/api/register',{
        method:"POST",
        headers:{
            "Content-Type" : "application/json"
        },
        body:JSON.stringify({
            nickname,
            password
        })
    })
    .then(res=>res.json())
    .then(data=>{
        alert(data.message);
    })
    .catch(error => {
        console.error(error);
    })
})