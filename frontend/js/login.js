async function loginUser() {

    const email =
        document.getElementById("email").value;

    const password =
        document.getElementById("password").value;
        const message =
        document.getElementById("message");

if(!email || !password){

    message.className = "error";

    message.innerText =
    "Please enter email and password";

    return;
}
    
    const response = await fetch(
        "https://pet-care-scheduler-avpb.onrender.com/users/login",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email,
                password
            })
        }
    );

    const data = await response.json();

    if(response.ok){

        localStorage.setItem(
            "loggedIn",
            "true"
        );

        localStorage.setItem(
            "full_name",
            data.full_name
        );

        localStorage.setItem(
            "user_email",
            data.email
        );

        localStorage.setItem(
            "user_id",
            data.user_id
        );
        localStorage.setItem(
            "token",
            data.access_token
        );
        message.innerText =
            "✅ Login Successful";

        message.style.color =
            "green";

        setTimeout(() => {
            window.location.href =
                "index.html";
        }, 1000);

    }
    else{

        message.innerText =
            "❌ " + data.detail;

        message.style.color =
            "red";
    }
}