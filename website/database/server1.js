/* const express = require('express'); // lightweight framework - for web servers
const fs = require('fs'); // file system access library
const path = require('path'); // manages file paths across different operating systems
const cors = require('cors');

const app = express(); // create instance, handles requests, responses, and routes

app.use(cors()); // uses cors for all requests
app.use(express.json()); // converts incoming JSON data (from fetch()) to JS object

app.use(express.static(path.join(__dirname, 'database')));

app.post('/save-account', (req, res) => { // POST request handler for URL /save-account, req = object containing frontend sent data, res = object allowing for response
    const { email, username, password } = req.body; // object destructuring
    console.log("Received data:", req.body);

    if (!email || !username || !password) {
        return res.status(400).json({ error: "All fields are required" });
    }

    const toWrite = `${email}|${username}|${password}\n`;
    const filePath = path.join(__dirname, `${username}`, `${username}Info.txt`); // formats/joins the path of the file and the dir/folder

    // Check if 'accounts' directory exists, create if it doesn't
    fs.mkdir(path.join(__dirname, 'database', `${username}`), { recursive: true }, (error) => {
        if (error) {
            return res.status(500).json({ error: "Error creating directory" });
        }

        // Append to the existing file
        fs.appendFile(filePath, toWrite, (error) => {
            if (error) {
                return res.status(500).json({ error: "Error saving data" });
            }
            res.json({ message: "Data saved successfully" });
        });
    });
});


let usernameGlobal = ""

app.post('/login', (req, res) => {
    const { username, password } = req.body;
    console.log("Received data:", req.body);

    usernameGlobal = username;

    if (!username || !password) {
        return res.status(400).json({ error: "Username and password are required" });
    }

    const filePath = path.join(__dirname, 'database', username, `${username}Info.txt`);

    fs.readFile(filePath, 'utf8', (error, data) => {
        if (error) {
            return res.status(400).json({ error: "User not found" });
        }

        const firstLine = data.split('\n')[0].trim();
        const [email, storedUsername, storedPassword] = firstLine.split('|');

        if (username === storedUsername && password === storedPassword) {
            res.json({ message: "Login successful", username });
        } else {
            res.status(401).json({ error: "Invalid username or password" });
        }
    }); 
});

app.post('/log-upload', (req, res) => {

    console.log("Received data:", req.body);
    const { month, day, burned, consumed, exercises } = req.body;
    console.log("Received data:", req.body);

    if (!burned || !consumed || !exercises){
        console.log("here");
        return res.status(400).json({ error: "All fields are required" });

    }

    const filePath = path.join(__dirname, 'database', usernameGlobal, `${usernameGlobal}Info.txt`);
    

    const toWrite = `${month}|${day}|${burned}|${consumed}|${exercises}`;
    fs.appendFile(filePath, toWrite, (error) => {
        if(error){
            return res.status(500).json({ error: "Error saving data" });
        }
        res.json({ message: "Data saved successfully"});
    })
})

const PORT = 3000;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`)); */
/*
const express = require('express');
const fs = require('fs').promises;
const path = require('path');
const cors = require('cors');


  
const app = express();

app.use(cors(), express.json(), express.static(path.join(__dirname, 'database')));
app.use(express.json());

const PORT = 3000;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));



// Serve static files from the 'database' directory



// POST route to save account information
app.post('/save-account', (req, res) => {
    const { email, username, password } = req.body;

    if (!email || !username || !password) {
        return res.status(400).json({ error: "All fields are required" });
    }

    const toWrite = `${email}|${username}|${password}\n`;
    const filePath = path.join(__dirname, 'database', username, `${username}Info.txt`);

    // Create user directory if it doesn't exist
    fs.mkdir(path.join(__dirname, 'database', username), { recursive: true }, (err) => {
        if (err) {
            return res.status(500).json({ error: "Error creating directory" });
        }

        // Append user data to the file
        fs.appendFile(filePath, toWrite, (err) => {
            if (err) {
                return res.status(500).json({ error: "Error saving data" });
            }
            res.json({ message: "Data saved successfully" });
        });
    });
});

// POST route for user login
let usernameGlobal = "";

app.post('/login', (req, res) => {
    const { username, password } = req.body;
    console.log('Login request received:', req.body); // Log the request body
    usernameGlobal = username;

    if (!username || !password) {
        return res.status(400).json({ error: "Username and password are required" });
    }

    const filePath = path.join(__dirname, 'database', username, `${username}Info.txt`);

    // Read the user file and check if credentials match
    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            return res.status(400).json({ error: "User not found" });
        }

        const [email, storedUsername, storedPassword] = data.split('\n')[0].split('|');

        if (username === storedUsername && password === storedPassword) {
            res.json({ message: "Login successful", username });
        } else {
            res.status(401).json({ error: "Invalid username or password" });
        }
    });
});

// POST route to save log data
app.post('/log-upload', (req, res) => {
    const { month, day, burned, consumed, exercises } = req.body;

    if (!burned || !consumed || !exercises) {
        return res.status(400).json({ error: "All fields are required" });
    }

    const filePath = path.join(__dirname, 'database', usernameGlobal, `${usernameGlobal}Info.txt`);
    const toWrite = `${month}|${day}|${burned}|${consumed}|${exercises}\n`;

    fs.appendFile(filePath, toWrite, (err) => {
        if (err) {
            return res.status(500).json({ error: "Error saving data" });
        }
        res.json({ message: "Data saved successfully" });
    });
});

app.post('/display-current', (req, res) => {
    const {date} = req.body;

    if(!date){
        return res.status(400).json({ error: "date not found" });
    }

    const filePath = path.join(__dirname, 'database', usernameGlobal, `${usernameGlobal}Info.txt`);

    fs.readFile(filePath, 'utf-8', (error, data) => {
        
        const months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
          ];

        if(error){
            return res.status(400).json({ error: "User not found" });
        }

        let foundData = null;

        const lines = data.split("\n");

        for(let line of lines){
            const parts = line.split("|");
            if (parts.length < 4) continue; // Skip invalid lines

            const month = parts[0];
            const day = parts[1];
            const burned = parts[2];
            const consumed = parts[3];
            const exercises = parts.slice(4); // Remaining elements are exercises

            if (`${month}|${day}` === date) {
                foundData = { month, day, burned, consumed, exercises };
                break;
            }
        }

        if(!foundData){
            return res.status(404).json({ error: "No data found for the given date" });
        }
        
        res.json({ message: "Data received successfully", data: foundData });
    })
}) 
*/

const express = require('express');
const AWS = require('aws-sdk');
const app = express();

const AWS = require('aws-sdk');
const dynamoDB = new AWS.DynamoDB.DocumentClient();

// Set up the POST route to save user data
app.post('/save-account', async (req, res) => {
    const { email, username, password } = req.body;

    if (!email || !username || !password) {
        return res.status(400).json({ error: "All fields are required" });
    }

    const params = {
        TableName: 'Users',  // Your DynamoDB table name
        Item: {
            username: username,
            email: email,
            password: password,
            trainingData: []  // Empty array for now; you can later append training data
        }
    };

    try {
        // Insert data into DynamoDB table
        await dynamoDB.put(params).promise();
        res.json({ message: "Account created successfully" });
    } catch (error) {
        console.error("Error saving account data:", error);
        res.status(500).json({ error: "Error saving account" });
    }
});

app.post('/login', async (req, res) => {
    const { username, password } = req.body;

    if (!username || !password) {
        return res.status(400).json({ error: "Username and password are required" });
    }

    const params = {
        TableName: 'Users',  // Your DynamoDB table name
        Key: {
            username: username  // Use the username to query for the user data
        }
    };

    try {
        const result = await dynamoDB.get(params).promise();
        const user = result.Item;

        if (!user || user.password !== password) {
            return res.status(401).json({ error: "Invalid username or password" });
        }

        res.json({ message: "Login successful", username });
    } catch (error) {
        console.error("Error fetching user data:", error);
        res.status(500).json({ error: "Error retrieving user data" });
    }
});



