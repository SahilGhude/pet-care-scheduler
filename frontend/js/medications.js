const API_URL = "http://127.0.0.1:8000/medications";

async function getMedications() {

    const userId =
    localStorage.getItem("user_id");

const response =
    await fetch(
        API_URL +
        "/user/" +
        userId
    );
    const medications = await response.json();

    const table = document.getElementById("medicationTable");

    table.innerHTML = "";

    medications.forEach(medication => {

        table.innerHTML += `
        <tr>
            <td>${medication.id}</td>
            <td>${medication.pet_id}</td>
            <td>${medication.pet_name}</td>
            <td>${medication.medicine_name}</td>
            <td>${medication.dosage}</td>
            <td>${medication.frequency}</td>
            <td>${medication.start_date}</td>
            <td>${medication.end_date}</td>
            <td>${medication.reminder_time}</td>

<td>
    <span class="badge ${medication.status.toLowerCase()}">
        ${medication.status}
    </span>
</td>
            <td>
                <button class="edit-btn"
                    onclick="editMedication(${medication.id})">
                    ✏️ Edit
                </button>

                <button class="delete-btn"
                    onclick="deleteMedication(${medication.id})">
                    🗑 Delete
                </button>
            </td>
        </tr>
        `;
    });

    document.getElementById("totalMedications").innerText =
        medications.length;
}

const form = document.getElementById("medicationForm");

form.addEventListener("submit", async function(event){

    event.preventDefault();

    const medicationId =
        document.getElementById("medicationId").value;

    const medication = {

        pet_id: parseInt(
            document.getElementById("pet_id").value
        ),

        medicine_name:
            document.getElementById("medicine_name").value,

        dosage:
            document.getElementById("dosage").value,

        frequency:
            document.getElementById("frequency").value,

        start_date:
            document.getElementById("start_date").value,

        end_date:
            document.getElementById("end_date").value,

        reminder_time:
            document.getElementById("reminder_time").value,

        status:
            document.getElementById("status").value
    };

    if(medicationId){

        await fetch(API_URL + "/" + medicationId,{
            method:"PUT",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify(medication)
        });

    }else{

        await fetch(API_URL + "/",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify(medication)
        });
    }

    form.reset();
    document.getElementById("medicationId").value = "";

    getMedications();
});

async function deleteMedication(id){

    if(!confirm("Delete this medication?")){
        return;
    }

    await fetch(API_URL + "/" + id,{
        method:"DELETE"
    });

    getMedications();
}

async function editMedication(id){

    const response = await fetch(API_URL + "/" + id);

    const medication = await response.json();

    document.getElementById("medicationId").value =
        medication.id;

    document.getElementById("pet_id").value =
        medication.pet_id;

    document.getElementById("medicine_name").value =
        medication.medicine_name;

    document.getElementById("dosage").value =
        medication.dosage;

    document.getElementById("frequency").value =
        medication.frequency;

    document.getElementById("start_date").value =
        medication.start_date;

    document.getElementById("end_date").value =
        medication.end_date;

    document.getElementById("reminder_time").value =
        medication.reminder_time;

    document.getElementById("status").value =
        medication.status;
}

getMedications();
async function loadPets() {

    const userId =
        localStorage.getItem("user_id");

    const response =
        await fetch(
            "http://127.0.0.1:8000/pets/user/" +
            userId
        );

    const pets =
        await response.json();
    const petSelect = document.getElementById("pet_id");

    petSelect.innerHTML =
        '<option value="">Select Pet</option>';

    pets.forEach(pet => {

        petSelect.innerHTML += `
            <option value="${pet.id}">
                ${pet.id} - ${pet.pet_name}
            </option>
        `;

    });

}
loadPets();
getMedications();