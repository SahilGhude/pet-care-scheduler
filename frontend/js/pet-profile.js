const params =
new URLSearchParams(
    window.location.search
);

const petId =
params.get("id");

async function loadPet() {

    // Pet Profile
    const response =
    await fetch(
        "http://127.0.0.1:8000/pets/profile/" +
        petId
    );

    const pet =
    await response.json();
document.getElementById(
    "petPhoto"
).src =
pet.photo_url ||
"https://via.placeholder.com/120";
    document.getElementById(
        "petName"
    ).innerText =
    pet.pet_name;
document.getElementById(
    "petIdText"
).innerText = pet.id;
    document.getElementById(
        "species"
    ).innerText =
    pet.species;

    document.getElementById(
        "breed"
    ).innerText =
    pet.breed;

    document.getElementById(
        "gender"
    ).innerText =
    pet.gender;

    document.getElementById(
        "age"
    ).innerText =
    pet.age;

    document.getElementById(
        "weight"
    ).innerText =
    pet.weight;

    document.getElementById(
        "vaccinations"
    ).innerText =
    pet.vaccinations;

    document.getElementById(
        "medications"
    ).innerText =
    pet.medications;

    document.getElementById(
        "appointments"
    ).innerText =
    pet.appointments;
document.getElementById(
    "healthScore"
).innerText =
pet.health_score + "/100";
if(pet.health_score >= 90){

    document.getElementById(
        "healthMessage"
    ).innerText =
    "Your pet is in excellent condition.";

}
else if(pet.health_score >= 70){

    document.getElementById(
        "healthMessage"
    ).innerText =
    "Your pet is healthy and doing well.";

}
else if(pet.health_score >= 50){

    document.getElementById(
        "healthMessage"
    ).innerText =
    "Some health records need attention.";

}
else{

    document.getElementById(
        "healthMessage"
    ).innerText =
    "Immediate attention is recommended.";

}
const badge =
document.getElementById(
    "healthStatus"
);

badge.innerText =
pet.health_status;
if (pet.health_score >= 90) {

    badge.style.background = "#22c55e";
    badge.style.color = "white";

}
else if (pet.health_score >= 70) {

    badge.style.background = "#3b82f6";
    badge.style.color = "white";

}
else if (pet.health_score >= 50) {

    badge.style.background = "#eab308";
    badge.style.color = "black";

}
else {

    badge.style.background = "#ef4444";
    badge.style.color = "white";

}
    // Health Score Card

const scoreCard =
document.querySelector(
    ".health-score-card"
);

if (pet.health_score >= 90) {

    scoreCard.style.background =
    "#22c55e";

}
else if (pet.health_score >= 70) {

    scoreCard.style.background =
    "#3b82f6";

}
else if (pet.health_score >= 50) {

    scoreCard.style.background =
    "#eab308";

}
else {

    scoreCard.style.background =
    "#ef4444";

}
    const historyResponse =
    await fetch(
        "http://127.0.0.1:8000/pets/" +
        petId +
        "/history"
    );

    const history =
    await historyResponse.json();

    // Vaccinations

    let vaccinationHtml = "";

    history.vaccinations.forEach(v => {

        vaccinationHtml += `
        <div class="history-card">
            <b>${v.vaccine_name}</b><br>

            Vaccination Date:
            ${v.vaccination_date}<br>

            Next Due:
            ${v.next_due_date}
        </div>
        `;
    });

    document.getElementById(
        "vaccinationHistory"
    ).innerHTML =
    vaccinationHtml;

    // Medications

    let medicationHtml = "";

    history.medications.forEach(m => {

        medicationHtml += `
        <div class="history-card">
            <b>${m.medicine_name}</b><br>

            Dosage:
            ${m.dosage}<br>

            Start:
            ${m.start_date}<br>

            End:
            ${m.end_date}
        </div>
        `;
    });

    document.getElementById(
        "medicationHistory"
    ).innerHTML =
    medicationHtml;

    // Appointments

    let appointmentHtml = "";

    history.appointments.forEach(a => {

        appointmentHtml += `
        <div class="history-card">
            Appointment ID:
            ${a.id}<br>

            Date:
            ${a.appointment_date}<br>

            Status:
            ${a.status}
        </div>
        `;
    });

    document.getElementById(
        "appointmentHistory"
    ).innerHTML =
    appointmentHtml;
}

loadPet();