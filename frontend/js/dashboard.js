if (
    localStorage.getItem("loggedIn")
    !== "true"
){
    window.location.href =
        "login.html";
}

document.addEventListener(
    "DOMContentLoaded",
    function(){

        const userName =
            document.getElementById("userName");

        if(userName){

            userName.innerText =
                localStorage.getItem(
                    "full_name"
                ) || "User";
        }
    }
);

const PET_API =
    "http://127.0.0.1:8000/pets";

const VACCINATION_API =
    "http://127.0.0.1:8000/vaccinations";

const MEDICATION_API =
    "http://127.0.0.1:8000/medications";

const APPOINTMENT_API =
    "http://127.0.0.1:8000/appointments";

async function loadDashboard() {

    try {

        const userId =
            localStorage.getItem("user_id");

        const pets =
            await fetch(
                `${PET_API}/user/${userId}`
            ).then(res => res.json());

        const vaccinations =
            await fetch(
                `${VACCINATION_API}/user/${userId}`
            ).then(res => res.json());

        const medications =
            await fetch(
                `${MEDICATION_API}/user/${userId}`
            ).then(res => res.json());

        const appointments =
            await fetch(
                `${APPOINTMENT_API}/user/${userId}`
            ).then(res => res.json());

        document.getElementById(
            "totalPets"
        ).innerText =
            pets.length;

        document.getElementById(
            "totalVaccinations"
        ).innerText =
            vaccinations.length;

        document.getElementById(
            "totalMedications"
        ).innerText =
            medications.length;

        document.getElementById(
            "totalAppointments"
        ).innerText =
            appointments.length;

        const today =
            new Date()
            .toISOString()
            .split("T")[0];

        const todayAppointments =
            appointments.filter(
                appointment =>
                    appointment.appointment_date === today
            );

        document.getElementById(
            "todayAppointments"
        ).innerText =
            todayAppointments.length;

        const todayVaccinations =
            vaccinations.filter(
                vaccination =>
                    vaccination.vaccination_date === today
            );

        document.getElementById(
            "todayVaccinations"
        ).innerText =
            todayVaccinations.length;

        const upcomingAppointments =
            appointments.filter(
                appointment =>
                    appointment.appointment_date > today
            );

        document.getElementById(
            "upcomingAppointments"
        ).innerText =
            upcomingAppointments.length;

        const recentTable =
            document.getElementById(
                "recentAppointments"
            );

        if (recentTable) {

            recentTable.innerHTML = "";

            appointments
                .slice(-5)
                .reverse()
                .forEach(appointment => {

                    recentTable.innerHTML += `
                    <tr>
                        <td>${appointment.pet_name}</td>
                        <td>${appointment.doctor_name}</td>
                        <td>${appointment.appointment_date}</td>
                    </tr>
                    `;
                });
        }

    } catch (error) {

        console.error(
            "Dashboard Error:",
            error
        );

        document.getElementById(
            "totalPets"
        ).innerText = "0";

        document.getElementById(
            "totalVaccinations"
        ).innerText = "0";

        document.getElementById(
            "totalMedications"
        ).innerText = "0";

        document.getElementById(
            "totalAppointments"
        ).innerText = "0";

        document.getElementById(
            "todayAppointments"
        ).innerText = "0";

        document.getElementById(
            "todayVaccinations"
        ).innerText = "0";

        document.getElementById(
            "upcomingAppointments"
        ).innerText = "0";
    }
}

function logout() {

    localStorage.removeItem(
        "loggedIn"
    );

    localStorage.removeItem(
        "user_id"
    );

    localStorage.removeItem(
        "full_name"
    );

    localStorage.removeItem(
        "user_email"
    );

    window.location.href =
        "login.html";
}

loadDashboard();