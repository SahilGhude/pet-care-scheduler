const API_URL = "http://127.0.0.1:8000/vaccinations";
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
async function getVaccinations() {

    const userId =
    localStorage.getItem("user_id");

const response =
    await fetch(
        API_URL +
        "/user/" +
        userId
    );
    const vaccinations = await response.json();

    const table = document.getElementById("vaccinationTable");

    table.innerHTML = "";

    vaccinations.forEach(vaccination => {

        table.innerHTML += `
        <tr>
            <td>${vaccination.id}</td>
            <td>${vaccination.pet_id}</td>
            <td>${vaccination.pet_name}</td>
            <td>${vaccination.vaccine_name}</td>
            <td>${vaccination.vaccination_date}</td>
            <td>${vaccination.next_due_date}</td>
            <td>
    <span class="badge ${vaccination.status.toLowerCase()}">
        ${vaccination.status}
    </span>
</td>
            <td>${vaccination.notes}</td>

            <td>
                <button onclick="editVaccination(${vaccination.id})">
                    ✏️ Edit
                </button>

                <button onclick="deleteVaccination(${vaccination.id})">
                    🗑 Delete
                </button>
            </td>
        </tr>
        `;
    });

    document.getElementById("totalVaccinations").innerText =
        vaccinations.length;
}

const form = document.getElementById("vaccinationForm");

form.addEventListener("submit", async function(event){

    event.preventDefault();

    const vaccinationId =
        document.getElementById("vaccinationId").value;

    const vaccination = {

        pet_id: parseInt(
            document.getElementById("pet_id").value
        ),

        vaccine_name:
            document.getElementById("vaccine_name").value,

        vaccination_date:
            document.getElementById("vaccination_date").value,

        next_due_date:
            document.getElementById("next_due_date").value,

        status:
            document.getElementById("status").value,

        notes:
            document.getElementById("notes").value
    };

    if(vaccinationId){

        await fetch(API_URL + "/" + vaccinationId,{
            method:"PUT",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify(vaccination)
        });

    } else {

        await fetch(API_URL + "/",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify(vaccination)
        });
    }

    form.reset();

    document.getElementById("vaccinationId").value = "";

    getVaccinations();
});

async function deleteVaccination(id){

    if(!confirm("Delete this vaccination?")){
        return;
    }

    await fetch(API_URL + "/" + id,{
        method:"DELETE"
    });

    getVaccinations();
}

async function editVaccination(id){

    const response = await fetch(API_URL + "/" + id);

    const vaccination = await response.json();

    document.getElementById("vaccinationId").value =
        vaccination.id;

    document.getElementById("pet_id").value =
        vaccination.pet_id;

    document.getElementById("vaccine_name").value =
        vaccination.vaccine_name;

    document.getElementById("vaccination_date").value =
        vaccination.vaccination_date;

    document.getElementById("next_due_date").value =
        vaccination.next_due_date;

    document.getElementById("status").value =
        vaccination.status;

    document.getElementById("notes").value =
        vaccination.notes;
}

loadPets();
getVaccinations();