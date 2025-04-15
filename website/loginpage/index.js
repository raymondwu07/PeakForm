 
 /*
 function submitInfo(){
    const username = document.getElementById("loginUsername").value.trim();
    const password = document.getElementById("loginPassword").value.trim();

    if (!username || !password) {
        alert("Please fill in all fields!");
        return;
    }

    // Send login data to the backend
    fetch('http://localhost:3000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === "Login successful") {
            sessionStorage.setItem("username", data.username);
            window.location.href = "../training-log/index.html";
        } else {
            alert("Login failed: " + data.error);
        }
    })
    .catch(error => {
        console.error("Fetch error:", error);
        alert("An error occurred. Please try again.");
    })

 }
 */



const submitBtn = document.getElementById("submitBtn");
submitBtn.addEventListener("click", (event) => {
    event.preventDefault();

    const email = document.getElementById("loginEmail").value.trim();
    const username = document.getElementById("loginUsername").value.trim();
    const password = document.getElementById("loginPassword").value.trim();

    if (!email || !username || !password) {
        alert("Please fill in all fields.");
        return;
    }

    fetch('http://localhost:3000/save-account', {  // Make sure this URL matches your server's
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, username, password })
    })
    .then(response => response.json())
    .then(data => {
        alert("Account created successfully!");
    })
    .catch(error => {
        console.error("Fetch error:", error);
        alert("An error occurred. Please try again.");
    });
});

