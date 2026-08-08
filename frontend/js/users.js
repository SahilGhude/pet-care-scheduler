const API_URL = "http://127.0.0.1:8000/users";

async function getUsers() {

    const response = await fetch(API_URL + "/");
    const users = await response.json();

    let table = document.getElementById("userTableBody");

    table.innerHTML = "";

    users.forEach(user => {

        table.innerHTML += `
        <tr>
            <td>${user.id}</td>
            <td>${user.full_name}</td>
            <td>${user.email}</td>
            <td>${user.phone}</td>
            <td>
                <button onclick="editUser(${user.id})" class="edit-btn">
                    ✏️ Edit
                </button>

                <button onclick="deleteUser(${user.id})" class="delete-btn">
                    🗑 Delete
                </button>
            </td>
        </tr>
        `;

    });

    document.getElementById("totalUsers").innerText = users.length;
}

getUsers();

const form = document.getElementById("userForm");

form.addEventListener("submit", async function(event){

    event.preventDefault();

    const userId = document.getElementById("userId").value;

    const user = {
    full_name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    phone: document.getElementById("phone").value,
    password: document.getElementById("password").value
};
    if(userId){

        await fetch(API_URL + "/" + userId,{
            method:"PUT",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify(user)
        });

    }else{

        await fetch(API_URL + "/",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify(user)
        });

    }

    form.reset();
    document.getElementById("userId").value="";

    getUsers();
});

async function editUser(id){

    const response = await fetch(API_URL + "/" + id);

    const user = await response.json();

    document.getElementById("userId").value = user.id;
    document.getElementById("name").value = user.full_name;
    document.getElementById("email").value = user.email;
    document.getElementById("phone").value = user.phone;
}

async function deleteUser(id){

    if(confirm("Are you sure?")){

        await fetch(API_URL + "/" + id,{
            method:"DELETE"
        });

        getUsers();
    }
}
const searchInput = document.getElementById("searchUser");

searchInput.addEventListener("keyup", function () {

    const filter = searchInput.value.toLowerCase();

    const rows = document.querySelectorAll("#userTableBody tr");

    rows.forEach(row => {

        const name = row.cells[1].innerText.toLowerCase();
        const email = row.cells[2].innerText.toLowerCase();

        if (
            name.includes(filter) ||
            email.includes(filter)
        ) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }

    });

});