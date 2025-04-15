

analyseBtn.addEventListener("click", () => {
    localStorage.setItem("analyse", "true")
    console.log("analysing")})

goBackBtn.addEventListener("click", () => {
    console.log("moving back");
    window.location.href = "http://127.0.0.1:5501/trainer/website/training-log/index.html";})




const analyseBtn = document.getElementById("moveToUploadBtn");
const goBackBtn = document.getElementById("goBackBtn");

analyseBtn.addEventListener("click", () => {
    localStorage.setItem("analyse", "true")});

goBackBtn.addEventListener("click", () => {
    localStorage.setItem("backToCalendar", "true")})



    document.getElementById("logText").textContent = "Please complete all fields";
    document.getElementById("selectedDay").textContent = "";

    if ('{data_json}' == "undefined"){{
        warningText = "No data to display for today"
        para.textContent = warningText;
        displayDiv.appendChild(para);
    }}

    else{{
        let burned = {burned}
        let consumed = {consumed}
        
        const caloriesDiv = document.createElement("div");
        caloriesDiv.setAttribute("id", "caloriesDiv");

        const burnedP = document.createElement("p");
        burnedP.setAttribute("id", "burnedP");

        const consumedP = document.createElement("p");
        consumedP.setAttribute("id", "consumedP");

        burnedP.textContent = burned;
        consumedP.textContent = consumed;

        caloriesDiv.appendChild(consumedP);
        caloriesDIv.appendChild(burnedP);

        let data = JSON.parse('{data_json}');

        let exerciseDivs = [];
        let exerciseParas = [];

        for(let j = 0; j <= Object.entries(data).length - 1; j+=3){{

            console.log(Object.entries(data));
            
            let exerciseDiv = document.createElement("div");
            exerciseDiv.name = `exerciseDiv{{j}}`;
            exerciseDiv.classList.add("exerciseDivs");

            let exerciseP = document.createElement("p");
            exerciseP.name = `exerciseP{{j}}`;
            exerciseP.classList.add("exerciseParas");

            exerciseP = displayText + Object.entries(data)[j][0] + ": " + Object.entries(data)[j][1] + " " + Object.entries(data)[j+1][0] + ": " + Object.entries(data)[j+1][1] + " " + Object.entries(data)[j+2][0] + ": " + Object.entries(data)[j+2][1] + "\\n";

            exerciseDivs[j] = exerciseDiv;
            exerciseParas[j] = exerciseP;

        }}}}
        for(let i = 0; i < exerciseDivs.length -1; i++){{
            displayDiv.appendChild(exerciseDivs[i]);
        }}