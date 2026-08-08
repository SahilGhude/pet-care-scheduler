async function sendOTP() {

    const email =
        document.getElementById("email").value;

    const message =
        document.getElementById("message");

    const response = await fetch(
        `http://127.0.0.1:8000/users/forgot-password?email=${email}`,
        {
            method: "POST"
        }
    );

    const data =
        await response.json();

    message.innerText =
        data.message;
}
async function verifyOTP() {

    const email =
        document.getElementById("email").value;

    const otp =
        document.getElementById("otp").value;

    const message =
        document.getElementById("message");

    const response = await fetch(
        `http://127.0.0.1:8000/users/verify-otp?email=${email}&otp=${otp}`,
        {
            method: "POST"
        }
    );

    const data =
        await response.json();

    if(response.ok){

        message.className = "success";

        message.innerText =
            "OTP Verified Successfully";

    }else{

        message.className = "error";

        message.innerText =
            data.detail;
    }
}
async function resetPassword() {

    const email =
        document.getElementById("email").value;

    const new_password =
        document.getElementById("new_password").value;

    const message =
        document.getElementById("message");

    const response = await fetch(
        `http://127.0.0.1:8000/users/reset-password?email=${email}&new_password=${new_password}`,
        {
            method: "POST"
        }
    );

    const data =
        await response.json();

    if(response.ok){

        message.className = "success";

        message.innerText =
            "Password Reset Successfully";

        setTimeout(() => {

            window.location.href =
                "login.html";

        }, 1500);

    }else{

        message.className = "error";

        message.innerText =
            data.detail;
    }
}