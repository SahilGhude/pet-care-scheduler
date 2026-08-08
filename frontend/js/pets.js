const API_URL = "https://pet-care-scheduler-avpb.onrender.com/pets";

const SUPABASE_URL =
"https://foobtedfwjvpfbmrozou.supabase.co";

const SUPABASE_KEY =
"sb_publishable_EmSJ-dEw_z0tHSR9pcV3uA_J-ujwjgk";

const supabaseClient =
window.supabase.createClient(
    SUPABASE_URL,
    SUPABASE_KEY
);
async function uploadPetPhoto() {

    const file =
    document.getElementById(
        "petPhoto"
    ).files[0];

    if (!file) {
        return null;
    }

    const fileName =
    Date.now() +
    "_" +
    file.name;

    const { error } =
    await supabaseClient.storage
    .from("pet-images")
    .upload(
        fileName,
        file
    );

    if (error) {
    console.error("Upload Error:", error);
    alert(error.message);
    return null;
}

    const { data } =
    supabaseClient.storage
    .from("pet-images")
    .getPublicUrl(
        fileName
    );

    return data.publicUrl;
}
// Get All Pets
async function getPets() {

    const userId =
    localStorage.getItem("user_id");

const response =
    await fetch(
        API_URL +
        "/user/" +
        userId
    );
    const pets =
await response.json();
    const table =
        document.getElementById("petTable");

    table.innerHTML = "";

    pets.forEach(pet => {

        table.innerHTML += `
        <tr>
            <td>${pet.id}</td>
            <td>${pet.pet_name}</td>
            <td>${pet.species}</td>
            <td>${pet.breed}</td>
            <td>${pet.age}</td>
            <td>${pet.weight}</td>

            <td>

    <button
        class="view-btn"
        onclick="
        window.location.href=
        'pet-profile.html?id=${pet.id}'
        ">
        👁 View
    </button>

    <button
        class="edit-btn"
        onclick="editPet(${pet.id})">
        ✏️ Edit
    </button>

    <button
        class="delete-btn"
        onclick="deletePet(${pet.id})">
        🗑 Delete
    </button>

</td>
        </tr>
        `;
    });

    document.getElementById(
        "totalPets"
    ).innerText = pets.length;
}

// Form Submit
const form =
    document.getElementById("petForm");

form.addEventListener(
    "submit",
    async function(event){

    event.preventDefault();

    const petId =
        document.getElementById("petId").value;
        const photoUrl =
    await uploadPetPhoto();

    const pet = {

    user_id: parseInt(
        localStorage.getItem("user_id")
    ),

    pet_name:
        document.getElementById("pet_name").value,

    species:
        document.getElementById("species").value,

    breed:
        document.getElementById("breed").value,

    gender:
        document.getElementById("gender").value,

    age: parseInt(
        document.getElementById("age").value
    ),

    weight: parseFloat(
        document.getElementById("weight").value
    ),

    photo_url: photoUrl
};

    if(petId){

        await fetch(
            API_URL + "/" + petId,
            {
                method: "PUT",
                headers: {
                    "Content-Type":
                    "application/json"
                },
                body: JSON.stringify(pet)
            }
        );

    } else {

        await fetch(
            API_URL + "/",
            {
                method: "POST",
                headers: {
                    "Content-Type":
                    "application/json"
                },
                body: JSON.stringify(pet)
            }
        );
    }

    form.reset();

    document.getElementById(
        "petId"
    ).value = "";

    getPets();
});

// Delete Pet
async function deletePet(id){

    if(!confirm(
        "Delete this pet?"
    )){
        return;
    }

    await fetch(
        API_URL + "/" + id,
        {
            method:"DELETE"
        }
    );

    getPets();
}

// Edit Pet
async function editPet(id){

    const response =
        await fetch(API_URL + "/" + id);

    const pet =
        await response.json();

    document.getElementById(
        "petId"
    ).value = pet.id;

    

    document.getElementById(
        "pet_name"
    ).value = pet.pet_name;

    document.getElementById(
        "species"
    ).value = pet.species;

    document.getElementById(
        "breed"
    ).value = pet.breed;

    document.getElementById(
        "gender"
    ).value = pet.gender;

    document.getElementById(
        "age"
    ).value = pet.age;

    document.getElementById(
        "weight"
    ).value = pet.weight;
   
}


getPets();
const searchInput =
    document.getElementById(
        "searchPet"
    );

searchInput.addEventListener(
    "keyup",
    function(){

    const filter =
        searchInput.value.toLowerCase();

    const rows =
        document.querySelectorAll(
            "#petTable tr"
        );

    rows.forEach(row => {

        const petName =
            row.cells[1]
            .innerText
            .toLowerCase();

        const species =
            row.cells[2]
            .innerText
            .toLowerCase();

        const breed =
            row.cells[3]
            .innerText
            .toLowerCase();

        if(
            petName.includes(filter) ||
            species.includes(filter) ||
            breed.includes(filter)
        ){
            row.style.display = "";
        }
        else{
            row.style.display = "none";
        }
    });
});