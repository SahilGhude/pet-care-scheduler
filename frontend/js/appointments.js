const API_URL = "https://pet-care-scheduler-avpb.onrender.com/appointments";
const PET_API = "https://pet-care-scheduler-avpb.onrender.com/pets";


async function loadPets() {

    const userId =
        localStorage.getItem("user_id");

    const response =
        await fetch(
            "https://pet-care-scheduler-avpb.onrender.com/pets/user/" +
            userId
        );

    const pets =
        await response.json();

    const petSelect =
        document.getElementById("pet_id");

    petSelect.innerHTML =
        `<option value="">
            Select Pet
        </option>`;

    pets.forEach(pet => {

        petSelect.innerHTML += `
        <option value="${pet.id}">
            ${pet.pet_name}
        </option>
        `;
    });
}


async function getAppointments() {

    const userId =
        localStorage.getItem("user_id");

    const response =
        await fetch(
            API_URL +
            "/user/" +
            userId
        );

    const appointments =
        await response.json();

    const table = document.getElementById("appointmentTable");

    table.innerHTML = "";

    appointments.forEach(appointment => {

        table.innerHTML += `
        <tr>
            <td>${appointment.id}</td>
            <td>${appointment.pet_id}</td>
            <td>${appointment.pet_name}</td>
            <td>${appointment.doctor_name}</td>
            <td>${appointment.clinic_name}</td>
            <td>${appointment.appointment_date}</td>
            <td>${appointment.appointment_time}</td>
            <td>${appointment.purpose}</td>
            <td>
    <span class="badge ${appointment.status.toLowerCase()}">
        ${appointment.status}
    </span>
</td>
            <td>${appointment.notes}</td>
            
            <td>
                <button onclick="editAppointment(${appointment.id})">
                    ✏️ Edit
                </button>

                <button onclick="deleteAppointment(${appointment.id})">
                    🗑 Delete
                </button>
            </td>
        </tr>
        `;
    });

    const totalAppointments =
        document.getElementById("totalAppointments");

    if (totalAppointments) {
        totalAppointments.innerText = appointments.length;
    }
}


const form = document.getElementById("appointmentForm");

form.addEventListener("submit", async function(event) {

    event.preventDefault();

    const appointmentId =
        document.getElementById("appointmentId").value;

    const appointment = {

        pet_id: parseInt(
            document.getElementById("pet_id").value
        ),

        doctor_name:
            document.getElementById("doctor_name").value,

        clinic_name:
            document.getElementById("clinic_name").value,

        appointment_date:
            document.getElementById("appointment_date").value,

        appointment_time:
            document.getElementById("appointment_time").value,

        purpose:
            document.getElementById("purpose").value,

        status:
            document.getElementById("status").value,

        notes:
            document.getElementById("notes").value
    };

    if (appointmentId) {

        await fetch(API_URL + "/" + appointmentId, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(appointment)
        });

    } else {

        await fetch(API_URL + "/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(appointment)
        });

    }

    form.reset();
    document.getElementById("appointmentId").value = "";

    getAppointments();
});


async function deleteAppointment(id) {

    if (!confirm("Delete this appointment?")) {
        return;
    }

    await fetch(API_URL + "/" + id, {
        method: "DELETE"
    });

    getAppointments();
}


async function editAppointment(id) {

    const response =
        await fetch(API_URL + "/" + id);

    const appointment =
        await response.json();

    document.getElementById("appointmentId").value =
        appointment.id;

    document.getElementById("pet_id").value =
        appointment.pet_id;

    document.getElementById("doctor_name").value =
        appointment.doctor_name;

    document.getElementById("clinic_name").value =
        appointment.clinic_name;

    document.getElementById("appointment_date").value =
        appointment.appointment_date;

    document.getElementById("appointment_time").value =
        appointment.appointment_time;

    document.getElementById("purpose").value =
        appointment.purpose;

    document.getElementById("status").value =
        appointment.status;

    document.getElementById("notes").value =
        appointment.notes;
}


loadPets();
getAppointments();