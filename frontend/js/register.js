async function registerUser() {
const message =
document.getElementById("message");
    const full_name =
        document.getElementById("full_name").value;

    const email =
        document.getElementById("email").value;

    const phone =
        document.getElementById("phone").value;

    const password =
        document.getElementById("password").value;

    if (
        !full_name ||
        !email ||
        !phone ||
        !password
    ) {
        message.className = "error";

message.innerText =
"Please fill all fields";
return;
    }

    try {

        const response = await fetch(
            "https://pet-care-scheduler-avpb.onrender.com/users/",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    full_name,
                    email,
                    phone,
                    password
                })
            }
        );

        const data = await response.json();

        if (response.ok) {

            const loginResponse = await fetch(
                "https://pet-care-scheduler-avpb.onrender.com/users/login",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        email: email,
                        password: password
                    })
                }
            );

            const loginData =
                await loginResponse.json();

            if (loginResponse.ok) {

                localStorage.setItem(
                    "loggedIn",
                    "true"
                );

                localStorage.setItem(
                    "user_id",
                    loginData.user_id
                );

                localStorage.setItem(
                    "full_name",
                    loginData.full_name
                );

                localStorage.setItem(
                    "email",
                    loginData.email
                );

                message.className = "success";

message.innerText =
"Registration Successful";

                setTimeout(() => {

    window.location.href =
    "dashboard.html";

}, 1000);

            } else {

               message.className = "error";

message.innerText =
"Auto Login Failed";
            }

        } else {

            message.className = "error";

message.innerText =
data.detail;

        }

    } catch (error) {

        console.error(error);

       message.className = "error";

message.innerText =
"Server Connection Error";

    }
}