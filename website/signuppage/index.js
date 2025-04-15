/* const passInput = document.getElementById("loginPassword");

function generatePass(){
    const possible = "abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+-=";
    let password = ""
    for(let i = 0; i <= 12; i++){
        password += possible[(Math.floor(Math.random()*49))+1]
    }

    passInput.value = password;
}
document.addEventListener("DOMContentLoaded", () => {
    const passBtn = document.getElementById("generateBtn");




    const email = document.getElementById("loginEmail").value;
    const username = document.getElementById("loginUsername").value;
    const password = document.getElementById("loginPassword").value;

    const submit = document.getElementById("submitBtn");

    submit.addEventListener("click", event => {
        event.preventDefault()

        fetch('http://localhost:3000/save-account', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: document.getElementById("loginEmail").value.trim(),
                username: document.getElementById("loginUsername").value.trim(),
                password: document.getElementById("loginPassword").value.trim()
            })
        })
        .then(response => response.json())
        .then(data => console.log("Response:", data))
        .catch(error => console.error("Fetch error:", error));
    });
    }
) */

/* // Generate password function
function generatePass() {
    const possible = "abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+-=";
    let password = "";
    for (let i = 0; i <= 12; i++) {
        password += possible[(Math.floor(Math.random() * possible.length))];
    }
    document.getElementById("loginPassword").value = password;
}

// Wait for the DOM to load
document.addEventListener("DOMContentLoaded", () => {
    // Attach event listener to the "Generate Password" button
    const generateBtn = document.getElementById("generateBtn");
    generateBtn.addEventListener("click", (event) => {
        event.preventDefault(); // Prevent any default button behavior
        generatePass(); // Call the password generation function
    });

    // Attach event listener to the "Create Account" button
    const submitBtn = document.getElementById("submitBtn");
    submitBtn.addEventListener("click", (event) => {
        event.preventDefault(); // Prevent form submission

        // Get the current values of the input fields
        const email = document.getElementById("loginEmail").value.trim();
        const username = document.getElementById("loginUsername").value.trim();
        const password = document.getElementById("loginPassword").value.trim();

        // Validate that all fields are filled
        if (!email || !username || !password) {
            alert("Please fill in all fields.");
            return;
        }

        // Send the data to the server
        fetch('http://localhost:3000/save-account', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, username, password })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Response:", data);
            alert("You have successfully created your account (database/username/usernameInfo.txt)");
        })
        .catch(error => {
            console.error("Fetch error:", error);
            alert("An error occurred. Please try again."); 
        });
    });

    // Attach event listener to the "Go Back" button
    const goBackBtn = document.getElementById("goBackBtn");
    goBackBtn.addEventListener("click", (event) => {
        event.preventDefault(); // Prevent default link behavior
        window.location.href = "../loginpage/index.html"; // Navigate to the login page
    });
});
*/


/*
document.addEventListener("DOMContentLoaded", () => {
    const generateBtn = document.getElementById("generateBtn");
    const submitBtn = document.getElementById("submitBtn");
    const goBackBtn = document.getElementById("goBackBtn");


    function generatePass() {
        const possible = "abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+-=";
        let password = "";
        for (let i = 0; i <= 12; i++) {
            password += possible[Math.floor(Math.random() * possible.length)];
        }
        document.getElementById("loginPassword").value = password;
    }


    generateBtn.addEventListener("click", (event) => {
        event.preventDefault();
        generatePass();
    });


    submitBtn.addEventListener("click", (event) => {
        event.preventDefault();

        const email = document.getElementById("loginEmail").value.trim();
        const username = document.getElementById("loginUsername").value.trim();
        const password = document.getElementById("loginPassword").value.trim();

        if (!email || !username || !password) {
            alert("Please fill in all fields.");
            return;
        }


        fetch('https://script.google.com/macros/s/AKfycbyck6IlM3VSmI2IzZxBXlp30cb_ttIApdrc1cUXrwy4Ze-0iMoVXQGtBy-wnxYy_hqHcA/exec', {
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


    goBackBtn.addEventListener("click", (event) => {
        event.preventDefault();
        window.location.href = "../loginpage/index.html";
    });
});
*/