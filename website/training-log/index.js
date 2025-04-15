const calendar = document.getElementById("calendar");
const dataEntry = document.getElementById("dataEntry");
const monthName = document.getElementById("monthName");
const daysContainer = document.getElementById("daysContainer");
const selectedDayElem = document.getElementById("selectedDay");
const exerciseInputsContainer = document.getElementById("exerciseInputs");
const addSetBtn = document.getElementById("addSetBtn");
const welcome = document.getElementById("welcomeHeader");

const months = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

let add = true;
let exerciseSetCount = 0;

function nextMonth(){
  let monthIndex = months.indexOf(monthName.textContent);
  if(monthIndex === 11){
    monthIndex = 0;
  }
  else{
    monthIndex +=1;
  }
  monthName.textContent = months[monthIndex];

}

function prevMonth(){
  let monthIndex = months.indexOf(monthName.textContent);
  if(monthIndex === 0){
    monthIndex = 11;
  }
  else{
    monthIndex -=1;
  }
  monthName.textContent = months[monthIndex];

}




function createCalendar() {
  for (let i = 1; i <= 12; i++) {
    const month = document.createElement("div");
    month.id = `month${i}`;
    calendar.appendChild(month);

    if (i !== 1) {
      month.classList.add("hidden");
    } else {
      monthName.textContent = months[i - 1];
    }

    const numDays = i === 2 ? 28 : (i % 2 === 0 ? 30 : 31);
    const daysContainer = document.createElement("div");
    daysContainer.classList.add("daysContainer");
    month.appendChild(daysContainer);

    for (let j = 1; j <= numDays; j++) {
      const dayBtn = document.createElement("button");
      dayBtn.classList.add("day");
      dayBtn.textContent = j;

      dayBtn.onclick = () => openDataEntry(j); 
      daysContainer.appendChild(dayBtn);
    }
  }
}


function openDataEntry(day) {
  selectedDayElem.textContent = day;
  calendar.classList.add("hidden");
  dataEntry.classList.remove("hidden");
  exerciseSetCount = 0; 
  exerciseInputsContainer.innerHTML = ''; 
  addExerciseInput(); 
}



function addExerciseInput() {

  exerciseSetCount++;

  const exerciseSetDiv = document.createElement("div");
  exerciseSetDiv.classList.add("exercise-set");

  const exerciseNameLabel = document.createElement("label");
  exerciseNameLabel.textContent = "Exercise Name:";
  const exerciseNameInput = document.createElement("input");
  exerciseNameInput.type = "text";

  exerciseNameInput.name = `exerciseName${exerciseSetCount}`;

  const weightLabel = document.createElement("label");
  weightLabel.textContent = "Weight:";
  const weightInput = document.createElement("input");
  weightInput.type = "number";
  weightInput.name = `weight${exerciseSetCount}`;

  const repsLabel = document.createElement("label");
  repsLabel.textContent = "Reps:";
  const repsInput = document.createElement("input");
  repsInput.type = "number";
  repsInput.name = `reps${exerciseSetCount}`;

  if(add){
    const consumedLabel = document.createElement("label");
    consumedLabel.textContent = "Calories Consumed: ";
    const consumedInput = document.createElement("input");
    consumedInput.type = "text";
    consumedInput.name = "consumed";
    const burnedLabel = document.createElement("label");
    burnedLabel.textContent = "Calories burned: ";
    const burnedInput = document.createElement("input");
    burnedInput.type = "text";
    burnedInput.name = "burned";

    exerciseSetDiv.appendChild(document.createElement("br"));
    exerciseSetDiv.appendChild(consumedLabel);
    exerciseSetDiv.appendChild(consumedInput);
    exerciseSetDiv.appendChild(document.createElement("br"));
    exerciseSetDiv.appendChild(burnedLabel);
    exerciseSetDiv.appendChild(burnedInput);
    exerciseSetDiv.appendChild(document.createElement("br"));

    add = false;
  }

  exerciseSetDiv.appendChild(document.createElement("br"));
  exerciseSetDiv.appendChild(exerciseNameLabel);
  exerciseSetDiv.appendChild(exerciseNameInput);
  exerciseSetDiv.appendChild(document.createElement("br"));


  exerciseSetDiv.appendChild(weightLabel);
  exerciseSetDiv.appendChild(weightInput);
  exerciseSetDiv.appendChild(document.createElement("br"));
  exerciseSetDiv.appendChild(repsLabel);
  exerciseSetDiv.appendChild(repsInput);


  exerciseInputsContainer.appendChild(exerciseSetDiv);
}



function submitData() {
  const dataMonth = monthName.textContent;
  const dataDay = selectedDayElem.textContent;
  const burned = document.querySelector(`input[name="burned"]`).value.trim();
  const consumed = document.querySelector(`input[name="consumed"]`).value.trim();
  let exerciseData = "";


  if (!burned || !consumed) {
    alert("Please fill out all fields (burned and consumed).");
    return;
  }


  for (let i = 1; i < exerciseSetCount + 1; i++) {
    const name = document.querySelector(`input[name="exerciseName${i}"]`).value.trim();
    const weight = document.querySelector(`input[name="weight${i}"]`).value.trim();
    const reps = document.querySelector(`input[name="reps${i}"]`).value.trim();

    if (!name || !weight || !reps) {
      alert("Please fill out all exercise fields.");
      return;
    }

    exerciseData += `${name}|${weight}|${reps}|`;
  }


  console.log({
    dataMonth,
    dataDay,
    burned,
    consumed,
    exerciseData
  });


  fetch("http://localhost:3000/log-upload", {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      month: dataMonth,
      day: dataDay,
      burned: burned,
      consumed: consumed,
      exercises: exerciseData
    })
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok ' + response.statusText);
    }
    return response.json();
  })
  .then(data => {
    console.log("Response:", data);
    alert("You have successfully logged your training in /database/username/usernameInfo.txt");
  })
  .catch(error => {
    console.error("Fetch error:", error);
    alert("An error occurred, please try again");
  });
}

function getData(){
  
}
function displayCurrent(){
  console.log("hi");
  const currentDate = `${monthName.textContent.trim()}|${selectedDayElem.textContent.trim()}`;

  console.log("currentDate:", currentDate);
  console.log("JSON being sent:", JSON.stringify({ date: currentDate }));

  fetch("http://localhost:3000/display-current", {
    method: 'POST',
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      date: currentDate
    }),
  })
  .then(response => {
    if(!response.ok){
      throw new Error('Network response was not ok ' + response.statusText);
    }
    response.json();
  })
  .then(data => {
    console.log("Response:", data);
  })
  .catch(error => {
    console.error("Fetch error:", error);
    alert("An error occurred, please try again");
  });
}

// Function to go back to the calendar view
function restoreCalendar() {
  calendar.classList.remove("hidden");
  dataEntry.classList.add("hidden");
}

createCalendar();

