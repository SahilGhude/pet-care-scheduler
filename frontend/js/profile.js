if (
    localStorage.getItem("loggedIn")
    !== "true"
){
    window.location.href =
        "login.html";
}

const userId =
    localStorage.getItem("user_id");

async function loadProfile() {

    try {

        const response =
            await fetch(
                "http://127.0.0.1:8000/users/" +
                userId
            );

        const user =
            await response.json();

        document.getElementById(
            "userId"
        ).value = user.id;

        document.getElementById(
            "fullName"
        ).value = user.full_name;

        document.getElementById(
            "email"
        ).value = user.email;

        document.getElementById(
            "phone"
        ).value = user.phone;

    } catch(error){

        console.error(
            "Profile Error:",
            error
        );
    }
}

document.getElementById(
    "editBtn"
).addEventListener(
    "click",
    function(){

        document.getElementById(
            "fullName"
        ).disabled = false;

        document.getElementById(
            "phone"
        ).disabled = false;

        document.getElementById(
            "passwordSection"
        ).style.display = "block";

        document.getElementById(
            "saveBtn"
        ).style.display =
            "inline-block";
    }
);

document.getElementById(
    "saveBtn"
).addEventListener(
    "click",
    async function () {

        const password =
            document.getElementById(
                "currentPassword"
            ).value;

        if (!password) {

            alert(
                "Please enter your current password"
            );

            return;
        }

        const updatedUser = {

            full_name:
                document.getElementById(
                    "fullName"
                ).value,

            email:
                document.getElementById(
                    "email"
                ).value,

            phone:
                document.getElementById(
                    "phone"
                ).value,

            password:
                password
        };

        try {

            const response =
                await fetch(
                    "http://127.0.0.1:8000/users/" +
                    userId,
                    {
                        method: "PUT",
                        headers: {
                            "Content-Type":
                                "application/json"
                        },
                        body: JSON.stringify(
                            updatedUser
                        )
                    }
                );

            if (response.ok) {

                alert(
                    "Profile Updated Successfully"
                );

                localStorage.setItem(
                    "full_name",
                    updatedUser.full_name
                );

                document.getElementById(
                    "fullName"
                ).disabled = true;

                document.getElementById(
                    "phone"
                ).disabled = true;

                document.getElementById(
                    "currentPassword"
                ).value = "";

                document.getElementById(
                    "passwordSection"
                ).style.display = "none";

                document.getElementById(
                    "saveBtn"
                ).style.display =
                    "none";

                loadProfile();

            } else {

                const error =
                    await response.json();

                alert(
                    error.detail
                );
            }

        } catch (error) {

            console.error(error);

            alert(
                "Failed to update profile"
            );
        }
    }
);

function logout(){

    localStorage.clear();

    window.location.href =
        "login.html";
}

loadProfile();