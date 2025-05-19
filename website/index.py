from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import os
import json
import cv2
import shutil
from ultralytics import YOLO
from angle_extractions import *
from angle_extractions import model

options = webdriver.ChromeOptions()
options.add_argument("--incognito")
 

#start web driver (chrome)
driver = webdriver.Chrome(options=options)

#HOME PAGE ---------------------------------------------------------------------------------------------------------------------------------------------------

driver.get("http://127.0.0.1:5501/trainer/website/homepage/index.html")


while True:

    print("start")

    if "homepage/index.html" in driver.current_url:

        driver.get("http://127.0.0.1:5501/trainer/website/homepage/index.html")

        driver.execute_script("""
            document.getElementById("toLoginBtn").addEventListener("click", () => {
                localStorage.setItem("loginClicked", "true");
                console.log("Go to Login clicked");
            });

            document.getElementById("toCreateBtn").addEventListener("click", () => {
                localStorage.setItem("createClicked", "true");
                console.log("Go to Signup clicked"); 
            });
        """)
        
        def checkLoginClicked():
            return driver.execute_script("""return localStorage.getItem('loginClicked');""")
        def checkCreateClicked():
            return driver.execute_script("""return localStorage.getItem("createClicked");""")
        
        while True:
            if checkLoginClicked() == "true":
                print("login")
                driver.execute_script("""
                                        localStorage.setItem("loginClicked", "false");
                                        window.location.href = "http://127.0.0.1:5501/trainer/website/loginpage/index.html";""")
                
                break
            elif checkCreateClicked() == "true":
                print("create")
                driver.execute_script("""
                                    localStorage.setItem("createClicked", "false");
                                    window.location.href = "http://127.0.0.1:5501/trainer/website/signuppage/index.html";
                                    """)
                break

            if "homepage/index.html" not in driver.current_url:
                    break

    #SIGNUP PAGE ---------------------------------------------------------------------------------------------------------------------------------------------------


    if "signuppage/index.html" in driver.current_url:
        
        print("signup")


        driver.get("http://127.0.0.1:5501/trainer/website/signuppage/index.html")


        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "goBackBtn")))


        driver.execute_script("""
            document.getElementById("submitBtn").addEventListener("click", function() {
                localStorage.setItem("submit", "true");

                const emailVal = document.getElementById("loginEmail").value;
                const userVal = document.getElementById("loginUsername").value;
                const passVal = document.getElementById("loginPassword").value;

                localStorage.setItem("email", emailVal);
                localStorage.setItem("username", userVal);
                localStorage.setItem("password", passVal);
            });

            document.getElementById("goBackBtn").addEventListener("click", function() {
                localStorage.setItem("goBack", "true");
            });
                              
            document.getElementById("login").addEventListener("click", function(){
                localStorage.setItem("goLogin", "true");
            });
                            
            document.getElementById("generateBtn").addEventListener("click", function() {
                const possible = "abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+-=";
                let password = "";
                for (let i = 0; i <= 12; i++) {
                    password += possible[Math.floor(Math.random() * possible.length)];
                }
                document.getElementById("loginPassword").value = password;
            });                  
        """)

        def checkGoLogin():
            return driver.execute_script("return localStorage.getItem('goLogin');")

        def checkSubmit():
            return driver.execute_script("return localStorage.getItem('submit');")
        
        def checkGoBack():
            return driver.execute_script("return localStorage.getItem('goBack');")


        def getEmail():
            return driver.execute_script("return localStorage.getItem('email');")

        def getUsername():
            return driver.execute_script("return localStorage.getItem('username');")

        def getPassword():
            return driver.execute_script("return localStorage.getItem('password');")





        while True:
            if checkGoBack() == "true":
                                driver.execute_script("""
                                            localStorage.setItem("goBack", "false");          
                                            window.location.href = "http://127.0.0.1:5501/trainer/website/homepage/index.html";""")
                                break
            elif checkGoLogin() == "true":
                                driver.execute_script("""
                                                        localStorage.setItem("goLogin", "false");
                                                        window.location.href = "http://127.0.0.1:5501/trainer/website/loginpage/index.html";""")
                                break
            elif checkSubmit() == "true":

                if len(str(getUsername())) != 0:
                    try:
                        user_dir = f"/Users/raymondwu/codingprograms/trainer/website/database/{str(getUsername())}"
                        if not os.path.isdir(user_dir):
                            os.mkdir(user_dir)

                            user_vids_dir = f"/Users/raymondwu/codingprograms/trainer/website/database/{str(getUsername())}/{str(getUsername())}-vids"
                            if not os.path.isdir(user_vids_dir):
                                os.mkdir(user_vids_dir)


                            try: 
                                open(f"/Users/raymondwu/codingprograms/trainer/website/database/{str(getUsername())}/{str(getUsername())}Data", "x").close()

                            except FileExistsError:
                                driver.execute_script("""
                                                    const signup = document.getElementById("signupTxt");
                                                    signup.textContent = "File already exists";""")

                            try:
                                with open(f"/Users/raymondwu/codingprograms/trainer/website/database/{str(getUsername())}/{str(getUsername())}Info", "w") as file:
                                    file.write(f"{str(getEmail())}|{str(getUsername())}|{getPassword()}")
                                    file.close()
                                driver.execute_script("""
                                                    const signup = document.getElementById("signupTxt");
                                                    signup.textContent = "Account Created!";

                                                    window.location.href = "http://127.0.0.1:5501/trainer/website/loginpage/index.html";""")
                                
                                break
                            
                            except FileExistsError:
                                driver.execute_script("""
                                                    const signup = document.getElementById("signupTxt");
                                                    signup.textContent = "File already exists";""")
        
                        
                        else:
                            driver.execute_script("""
                                                    const signup = document.getElementById("signupTxt");
                                                    signup.textContent = "Username already exists";
                                                    """)

                            if checkGoBack() == "true":
                                driver.execute_script("""
                                            window.location.href = "http://127.0.0.1:5501/trainer/website/loginpage/index.html";
                                                       """)
                                break

                    
                    except Exception as e:
                        print(f"Error creating directory: {e}")
                        driver.execute_script("""
                                                const signup = document.getElementById("signupTxt");
                                                signup.textContent = "Error";""")

                    

                else:
                    driver.execute_script("""
                                                const signup = document.getElementById("signupTxt");
                                                signup.textContent = "Enter a valid username please";""")

            if "signuppage/index.html" not in driver.current_url:
                    break



    #LOGIN PAGE ---------------------------------------------------------------------------------------------------------------------------------------------------

    if "/loginpage/index.html" in driver.current_url:

        print("login")

        driver.get("http://127.0.0.1:5501/trainer/website/loginpage/index.html")


        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "submitBtn")))


        driver.execute_script("""
            document.getElementById("submitBtn").addEventListener("click", () => {
                localStorage.setItem("submit", "true");

                const userVal = document.getElementById("loginUsername").value;
                const passVal = document.getElementById("loginPassword").value;

                localStorage.setItem("username", userVal);
                localStorage.setItem("password", passVal);
            });
            document.getElementById("signup").addEventListener("click", () => {
                localStorage.setItem('goBackSignIn', "true")
                              })

        """)


        def checkSubmit():
            return driver.execute_script("return localStorage.getItem('submit');")
        
        def checkGoBack():
            return driver.execute_script("return localStorage.getItem('goBackSignIn');")
        
        def checkSignUp():
            return driver.execute_script("return localStorage.getItem('goBackSignIn');")

        def getUsername():
            return driver.execute_script("return localStorage.getItem('username');")

        def getPassword():
            return driver.execute_script("return localStorage.getItem('password');")
        



        while True:
            if checkSignUp() == "true":
                driver.execute_script("""
                                            localStorage.setItem("goBackSignIn", "false");
                                            window.location.href = "http://127.0.0.1:5501/trainer/website/signuppage/index.html";
                                                       """)
                break
            elif checkSubmit() == "true":

                if len(str(getUsername())) != 0:
                    try:
                        user_dir = f"/Users/raymondwu/codingprograms/trainer/website/database/{str(getUsername())}"
                        if not os.path.isdir(user_dir):
                            driver.execute_script("""
                                    const loginTxt = document.getElementById("loginTxt");
                                    loginTxt.textContent = "Account doesn't exist"; """)
                        else:
                            try:
                                user_file = f"/Users/raymondwu/codingprograms/trainer/website/database/{str(getUsername())}/{str(getUsername())}Info"
                                with open(user_file, "r") as file:
                                    details = file.readline().split("|")
                                file.close()

                                if str(getUsername()) == details[1] and str(getPassword()) == details[2]:
                                    driver.execute_script("""

                                        window.location.href = "http://127.0.0.1:5501/trainer/website/training-log/index.html";
                                        """)
                                    break
                                else:
                                    driver.execute_script("""
                                    const loginTxt = document.getElementById("loginTxt");
                                    loginTxt.textContent = "Incorrect username or password"; """)
                            except IOError:
                                driver.execute_script("""
                                    const loginTxt = document.getElementById("loginTxt");
                                    loginTxt.textContent = "file not found"; """)
                    except Exception as e:
                        print(f"Error creating directory: {e}")
            
            if checkGoBack() == "true":
                driver.execute_script("""
                                        localStorage.setItem("goBackSignIn", "false");
                                        window.location.href = "http://127.0.0.1:5501/trainer/website/signuppage/index.html";
                                        """)
                break


            if "/loginpage/index.html" not in driver.current_url:
                break


                #stops the script but keep the browser open


    #TRAINING LOG PAGE ---------------------------------------------------------------------------------------------------------------------------------------------------

    if "/training-log/index.html" in driver.current_url:

        print("training log")

        driver.get("http://127.0.0.1:5501/trainer/website/training-log/index.html")


        driver.execute_script("""
                            const header = document.getElementById("welcomeHeader");
                            header.textContent = `Welcome ${localStorage.getItem("username")}`;""")

        driver.execute_script("""
                            const submitData = document.getElementById("submitData");
                            const displayBtn = document.getElementById("displayCurrentBtn");
                            const moveToUploadBtn = document.getElementById("moveToUploadBtn")
                            localStorage.setItem("displayClicked", "false");

                            submitData.addEventListener("click", () => {

                                const exerciseCount = returnExerciseCount();
                                localStorage.setItem("burned", returnBurned());
                                localStorage.setItem("consumed", returnConsumed());
                                
                                for(let i = 1; i <= exerciseCount; i++){ 
                                    console.log(i);
                                    localStorage.setItem(`name${i}`, document.getElementById(`exerciseName${i}`).value.trim());
                                    localStorage.setItem(`weight${i}`, document.getElementById(`weight${i}`).value.trim());
                                    localStorage.setItem(`reps${i}`, document.getElementById(`reps${i}`).value.trim());
                                }
                                
                                localStorage.setItem("submitLog", "true");
                            })
                            
                            displayBtn.addEventListener("click", () => {localStorage.setItem("displayClicked", "true")});
                            moveToUploadBtn.addEventListener("click", () => {console.log("to upload");
                                                                            localStorage.setItem("moveToUpload", "true")});
                              
                            
        """)



        def getUsername():
            return driver.execute_script(f"""return localStorage.getItem("username");""")
        
        def getConsumed():
            return driver.execute_script(f"""return localStorage.getItem("consumed");""")
        
        def getBurned():
            return driver.execute_script(f"""return localStorage.getItem("burned");""")
        
        def getName(num):
            return driver.execute_script(f"""return localStorage.getItem("name{num}");""")
            
        def getWeight(num):
            return driver.execute_script(f"""return localStorage.getItem("weight{num}");""")
        
        def getReps(num):
            return driver.execute_script(f"""return localStorage.getItem("reps{num}");""")
        
        def getExerciseCount():
            return driver.execute_script("""return returnExerciseCount();""")
        
        def getDate():
            date = driver.execute_script("""return document.getElementById("selectedDay").textContent.trim();""").strip()
            date = date.split(" ")

            return f"{date[0]}|{date[1]}"

        
        def checkDisplayBtnStatus():
            return driver.execute_script("""return localStorage.getItem("displayClicked");""")
        
        def moveToUpload():
            return driver.execute_script("""return localStorage.getItem("moveToUpload")""")
        
        def goBackToCalendar():
            return driver.execute_script("""return localStorage.getItem("ToCalendar");""")
        
        def checkSubmit():
            return driver.execute_script("""return localStorage.getItem("submitLog");""")
        

        driver.execute_script("""localStorage.setItem("submit", "false");""")


        while True:
            driver.execute_script("""
                                  const displayBtn = document.getElementById("displayCurrentBtn");
                                  const submitData = document.getElementById("submitData");
                                  const moveToUploadBtn = document.getElementById("moveToUploadBtn")
                                  
                                  submitData.addEventListener("click", () => {

                                    const exerciseCount = returnExerciseCount();
                                    localStorage.setItem("burned", returnBurned());
                                    localStorage.setItem("consumed", returnConsumed());
                                    
                                    for(let i = 1; i <= exerciseCount; i++){ 
                                        console.log(i);
                                        localStorage.setItem(`name${i}`, document.getElementById(`exerciseName${i}`).value.trim());
                                        localStorage.setItem(`weight${i}`, document.getElementById(`weight${i}`).value.trim());
                                        localStorage.setItem(`reps${i}`, document.getElementById(`reps${i}`).value.trim());
                                    }
                                    
                                    localStorage.setItem("submitLog", "true");
                                    })
                                  displayBtn.addEventListener("click", () => {localStorage.setItem("displayClicked", "true")});
                                  moveToUploadBtn.addEventListener("click", () => {console.log("to upload");
                                  localStorage.setItem("moveToUpload", "true")});
                                  """)
            
            if checkSubmit() ==  "true":
                driver.execute_script("localStorage.setItem('submitLog', 'false');")
                driver.execute_script("localStorage.setItem('displayClicked', 'false');")
                print("submitted")
                try:

                    path = f"/Users/raymondwu/codingprograms/trainer/website/database/{getUsername()}/{getUsername()}Data"
                    with open(path, "a") as file:
                        if getConsumed() == "" or getBurned() == "" or getName(1) == "" or getWeight(1) == "" or getReps(1) == "":
                            driver.execute_script("""
                                    prevtext = document.getElementById("welcomeHeader").textContent;
                                    document.getElementById("welcomeHeader").textContent = "Please complete all fields";
                                    setTimeout(() => {document.getElementById("welcomeHeader").textContent = prevtext}, 4000);
                                    """)
                        else:
                            for i in range(1, getExerciseCount()+1, 1):
                                file.write(f"{getName(i)}|{getWeight(i)}|{getReps(i)}|")
                            file.write(f"{getDate()}|{getConsumed()}|{getBurned()}|\n")

                            file.close()

                except IOError:
                    print("File not found")


            if checkDisplayBtnStatus() == "true":
                print("displaying")
                driver.execute_script("localStorage.setItem('displayClicked', 'false');")
                driver.execute_script("""document.getElementById("goBackBtn2").classList.remove("hidden");""")
                try:
                    path = f"/Users/raymondwu/codingprograms/trainer/website/database/{getUsername()}/{getUsername()}Data"
                    with open(path, "r") as file2:
                        data_json = "undefined"
                        data = {}

                        burned = ""
                        consumed = ""
                        for line in file2:

                            if getDate() in line:

                                exerciseData = line.strip().split("|")

                                consumed = exerciseData[len(exerciseData)-3]
                                burned = exerciseData[len(exerciseData)-2]
                                
                                num = 1
                                count = 1
                                for i in range(0, len(exerciseData)-5, 3):
                                    count += 1

                                    data[f"exerciseName{num}"] = exerciseData[i]
                                    data[f"weight{num}"] = exerciseData[i+1]
                                    data[f"reps{num}"] = exerciseData[i+2]

                                    num += 1

                                data_json = json.dumps(data)

                                driver.execute_script("""
                                    const displayPara = document.getElementById("displayPara");
                                    
                                    if(displayPara?.classList.contains("hidden")){{
                                        displayPara.classList.remove("hidden")}}
                                    
                                                    """)
                        file.close()
                    try:
                        if type(data_json) == "string":
                            pass
                    except NameError:
                        data_json = "undefined"
                    else:
                        pass
                    
                    script1 = f"""

                        
                                        
                        const entryWrapper = document.getElementById("dataEntry");
                        entryWrapper.classList.add("hidden");

                        const displayDiv = document.createElement("div");
                        displayDiv.setAttribute("id", "displayDiv");

                        let index = 0;

                        let topText = ""

                        const displayh2 = document.createElement("h2");
                        const h2Div = document.createElement("div");

                        h2Div.setAttribute("id", "h2Div");
                        displayh2.setAttribute("id", "displayh2");

                        h2Div.appendChild(displayh2);



                        if ('{data_json}' == "undefined"){{
                            topText = "No data to display for today";
                            displayh2.textContent = topText;
                            displayDiv.appendChild(h2Div);
                        }}

                        else{{
                            let burned = "{burned} calories burned"
                            let consumed = "{consumed} calories consumed"

                            let date = document.getElementById("selectedDay").textContent;

                            topText = `${{date}}`;
                            displayh2.textContent= topText;

                            const caloriesDiv = document.createElement("div");
                            caloriesDiv.setAttribute("id", "caloriesDiv");

                            const burnedP = document.createElement("p");
                            burnedP.setAttribute("id", "burnedP");

                            const consumedP = document.createElement("p");
                            consumedP.setAttribute("id", "consumedP");

                            burnedP.textContent = burned;
                            consumedP.textContent = consumed;

                            caloriesDiv.appendChild(consumedP);
                            caloriesDiv.appendChild(burnedP);

                            displayDiv.appendChild(h2Div);
                            displayDiv.appendChild(caloriesDiv);

                            let data = JSON.parse('{data_json}');


                            for(let j = 0; j <= Object.entries(data).length - 1; j+=3){{


                                
                                let exerciseDiv = document.createElement("div");
                                exerciseDiv.name = `exerciseDiv{{j}}`;
                                exerciseDiv.classList.add("exerciseDivs");

                                let exerciseP = document.createElement("p");
                                exerciseP.name = `exerciseP{{j}}`;
                                exerciseP.classList.add("exerciseParas");

                                exerciseP.textContent = Object.entries(data)[j][1].charAt(0).toUpperCase() +
                                                        Object.entries(data)[j][1].slice(1, Object.entries(data)[j][1].length) + 
                                                        ":  " + 
                                                        Object.entries(data)[j+1][1] + 
                                                        "kg for " + 
                                                        Object.entries(data)[j+2][1] + 
                                                        " reps";

                                exerciseDiv.appendChild(exerciseP);
                                displayDiv.appendChild(exerciseDiv);

                            }}}}



                            
                            const toCalendar = document.createElement("button");
                            toCalendar.textContent = "Go Back"; 
                            toCalendar.setAttribute("id", "toCalendar");


                            document.body.insertBefore(displayDiv, document.getElementById("footer"));
                            document.body.insertBefore(toCalendar, document.getElementById("footer"));

                            toCalendar.addEventListener("click", () => {{
                                displayDiv.classList.add("hidden");
                                entryWrapper.classList.remove("hidden");
                                toCalendar.classList.add("hidden");
                                localStorage.setItem("toCalendar", "true")
                            }})
                            """


                    driver.execute_script(script1)

                except IOError:
                    print("File not found")
                    driver.execute_script("""localStorage.clear();""")
                    break

            if moveToUpload() == "true":
                driver.execute_script("""
                                        localStorage.setItem("moveToUpload", "false");
                                        window.location.href = "http://127.0.0.1:5501/trainer/website/file-upload/index.html";
                                    """)
                break
            
            if "/training-log/index.html" not in driver.current_url:
                break





    #FILE UPLOAD PAGE ---------------------------------------------------------------------------------------------------------------------------------------------------

    if "/file-upload/index.html" in driver.current_url:

        print("file upload")

        driver.get("http://127.0.0.1:5501/trainer/website/file-upload/index.html")
        
        def checkGoBack():
            return driver.execute_script("""return localStorage.getItem("backToCalendar");""")
        
        def checkAnalyse():
            return driver.execute_script("""return localStorage.getItem("analyse");""")
        
        def checkUpload():
            return driver.execute_script("""return localStorage.getItem("upload"); """)
        
        
        def video_to_frames(video_path):
            filename = os.path.splitext(os.path.basename(video_path))[0]
            output_folder = f"/Users/raymondwu/codingprograms/trainer/website/database/{str(getUsername())}/{str(getUsername())}-vids/{filename}-frames"
            target_fps = 15
            cap = cv2.VideoCapture(video_path)

            if not cap.isOpened():
                print("Error: Cannot open video")
                return
            
            original_fps = cap.get(cv2.CAP_PROP_FPS) 
            frame_interval = int(original_fps / target_fps)

            if frame_interval < 1:
                frame_interval = 1

            os.makedirs(output_folder, exist_ok=True)

            frame_count = 0
            saved_count = 0

            while True:
                ret, frame = cap.read() 
                if not ret:
                    break

                if frame_count % frame_interval == 0:
                    frame_filename = os.path.join(output_folder, f"frame_{saved_count:05d}.jpg") 
                    cv2.imwrite(frame_filename, frame)
                    saved_count += 1

                frame_count += 1

            print(f"Saved {saved_count} frames to {output_folder}")
        

        while True:
            driver.execute_script("""const analyseBtn = document.getElementById("analyseBtn");
                                    const goBackBtn = document.getElementById("goBackBtn");
                                    const videoThumbnail = document.getElementById("videoThumbnail");
                                    const inputBtn = document.getElementById("inputBtn");
                                    const fileInput = document.getElementById("fileInput");
                                  
                                    localStorage.setItem("upload", "false");
                                    localStorage.setItem("analyse", "false");

                                    analyseBtn.addEventListener("click", () => {
                                        localStorage.setItem("analyse", "true")});

                                    goBackBtn.addEventListener("click", () => {
                                        localStorage.setItem("backToCalendar", "true")})
                                
                                    fileInput.addEventListener("change", () => {
                                            localStorage.setItem("upload", "true");
                                            })

                                    
                                """)

            if checkGoBack() == "true":
                driver.execute_script("""
                                    localStorage.setItem("backToCalendar", "false");
                                    
                                    if (localStorage.getItem("upload" == "true")){
                                        document.getElementById("fileInput").value = '';
                                        document.getElementById("inputBtn").display = "inline-flex";
                                        document.getElementById("videoThumbnail").style.display = "none";
                                        document.getElementById("videoThumbnail").src = "";
                                        localStorage.setItem("upload", "false");
                                    }  
                                      
                                    if (localStorage.getItem("analyse") == "true"){
                                        localStorage.setItem("analyse", "false");
                                      }
                                    window.location.href = "http://127.0.0.1:5501/trainer/website/training-log/index.html";
                                """)
                


                break

            if checkAnalyse() == "true":
                print("click")
                video_name = driver.execute_script(""" return localStorage.getItem("uploadedVideo"); """)

                if type(video_name) != str:
                    driver.execute_script("""
                                const myh3 = document.getElementById("myh3");
                                prevText = myh3.textContent;
                                myh3.textContent = "Please upload a video before analysing";
                                setTimeout(() => {myh3.textContent = prevText}, 4000)
                                          """)

                else:

                    filename = os.path.splitext(video_name)[0]
                    filetype = os.path.splitext(video_name)[1]
                    output_folder = f"/Users/raymondwu/codingprograms/trainer/website/database/{str(getUsername())}/{str(getUsername())}-vids"
                    driver.execute_script(f"""localStorage.setItem("file_name", "{filename}");""")

                    src_path = f"/Users/raymondwu/codingprograms/trainer/project-input/{video_name}"
                    video_path = f"/Users/raymondwu/codingprograms/trainer/website/database/{str(getUsername())}/{str(getUsername())}-vids/{filename + "_use" + filetype}"

                    shutil.copy2(src_path, video_path)


                    print("analysing")

                    driver.execute_script("""window.location.href = "http://127.0.0.1:5501/trainer/website/analysispage/index.html";""")

            if checkUpload() == "true":


                driver.execute_script("""
                                     const videoThumbnail = document.getElementById("videoThumbnail");
                                     const inputBtn = document.getElementById("inputBtn");
                                     const file = fileInput.files[0];
                                     if (file && file.type.startsWith('video/')) {
                                        localStorage.setItem("uploadedVideo", file.name);
                                        const videoURL = URL.createObjectURL(file);
                                        videoThumbnail.src = videoURL;
                                        videoThumbnail.style.display = "block";
                                        videoThumbnail.controls = true;
                                        inputBtn.style.display = "none";
                                        localStorage.setItem("upload", "false");
                                      }
                                     """)
                
                print("uploaded")

            if "/file-upload/index.html" not in driver.current_url:
                break


    #ANALYSIS PAGE ---------------------------------------------------------------------------------------------------------------------------------------------------

    if "/analysispage/index.html" in driver.current_url:

        print("analysis page")

        driver.get("http://127.0.0.1:5501/trainer/website/analysispage/index.html")

        driver.execute_script("""
                    goBackBtn = document.getElementById("goBackBtn");
                    deadliftBtn = document.getElementById("deadliftBtn");
                    squatBtn = document.getElementById("squatBtn");
                    pullupBtn = document.getElementById("pullupBtn");


                    goBackBtn.addEventListener("click", () => {
                              localStorage.setItem("backToUpload", "true")})
                    deadliftBtn.addEventListener("click", () => {
                              localStorage.setItem("deadlift", "true")})
                    squatBtn.addEventListener("click", () => {
                              localStorage.setItem("squat", "true")})
                    pullupBtn.addEventListener("click", () => {
                              localStorage.setItem("pullup", "true")})
                """)
        
        def checkDeadlift():
            return driver.execute_script("""
                    return localStorage.getItem("deadlift");
                                         """)

        def checkSquat():
            return driver.execute_script("""
                    return localStorage.getItem("squat");
                                         """)
    
        def checkPullup():
            return driver.execute_script("""
                    return localStorage.getItem("pullup");
                                            """)
        
        def checkGoBack():
            return driver.execute_script("""
                                         return localStorage.getItem("backToUpload");
                                         """)
        

        def find_file_by_name(folder_path, filename_without_extension):
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    name_only, _ = os.path.splitext(file)
                    if name_only == filename_without_extension:
                        return os.path.join(root, file)
            return None
        
        analyse_count_pullup = 0
        analyse_count_squat = 0
        analyse_count_deadlift = 0
        
        while True:
            print("analysing")
            if checkPullup() == "true":
                print("doing pullup")
                video_name = driver.execute_script("""return localStorage.getItem("uploadedVideo")""").split(".") 
                video_name = video_name[0]
                video_name += "_use"
                print(video_name)
                video_path = find_file_by_name(f"/Users/raymondwu/codingprograms/trainer/website/database/{str(getUsername())}/{str(getUsername())}-vids", video_name)

                if video_path == None:
                    print("video not found")
                
                else:
                    if analyse_count_pullup == 0:
                        results = model.predict(video_path, show=False, save=False)
                        analysed_video_path = f"/Users/raymondwu/codingprograms/trainer/runs/pose/predict/imperfect_pull.mp4"

                        x, y = get_coords_pullups(results)
                        nframes = len(results)
                        leftShoulders, rightShoulders = get_shoulders_coords(nframes, x, y)
                        leftElbows, rightElbows = get_elbows_coords(nframes, x, y)
                        leftWrists, rightWrists = get_wrists_coords(nframes, x, y)
                        left_angles = get_all_angles(nframes, leftShoulders, leftElbows, leftWrists)
                        right_angles = get_all_angles(nframes, rightShoulders, rightElbows, rightWrists)
                        analyse_count_pullup += 1

                        if not pullup_left_vs_right_all(left_angles, right_angles):
                            print("make an even strength distribution")
                            pass

                        if not check_ratio_pullups(left_angles):
                            print("slow down eccentric")
                            pass

            if checkSquat() == "true":
                print("doing squat")
                video_name = driver.execute_script("""return localStorage.getItem("uploadedVideo")""").split(".") 
                video_name = video_name[0]
                video_name += "_use"
                print(video_name)
                video_path = find_file_by_name(f"/Users/raymondwu/codingprograms/trainer/website/database/{str(getUsername())}/{str(getUsername())}-vids", video_name)

                if video_path == None:
                    print("video not found")
                
                else:
                    if analyse_count_squat == 0:
                        analyse_count_squat += 1
                        results = model.predict(video_path, show=True, save=False)
                        analysed_video_path = f"/Users/raymondwu/codingprograms/trainer/runs/pose/predict/imperfect_pull.mp4"

                        x, y = get_coords_squat(results)
                        nframes = len(results)
                        leftShoulders, rightShoulders = get_shoulders_coords(nframes, x, y)
                        leftHips, rightHips = get_hip_coords(nframes, x, y)
                        leftKnees, rightKnees = get_knee_coords(nframes, x, y)
                        leftAnkles, rightAnkles = get_ankle_coords(nframes, x, y)
                        noses = get_nose_coords(nframes, x, y)
                        left_angles = get_all_angles(nframes, leftHips, leftKnees, leftAnkles)
                        right_angles = get_all_angles(nframes, rightHips, rightKnees, rightAnkles)
                        squat_direction = get_squat_direction(nframes, noses, rightHips)

                        if squat_direction == "left":

                            start_ecc, stop_ecc = find_eccentric_squats(left_angles)
                            start_con, stop_con = stop_ecc, start_ecc

                            if not check_all_squat_align(nframes, noses, leftShoulders, leftAnkles):
                                print("Have shoulders/bar over midfoot for optimimal stability/bar path")

                            if not check_all_bentover(nframes, leftShoulders, leftHips, leftAnkles):
                                print("You are too bentover, be more upright during the motion")
                        
                            if not squat_depth_check(left_angles, stop_ecc):
                                print("You need to squat deeper")

                            if not check_ratio_squats(left_angles):
                                print("slow down eccentric")
                                pass
                        
                        elif squat_direction == "right":

                            start_ecc, stop_ecc = find_eccentric_squats(right_angles)
                            start_con, stop_con = stop_ecc, start_ecc

                            if not check_all_squat_align(nframes, noses, rightShoulders, rightAnkles):
                                print("Have shoulders/bar over midfoot for optimimal stability/bar path")

                            if not check_all_bentover(nframes, rightShoulders, rightHips, rightAnkles):
                                print("You are too bentover, be more upright during the motion")

                            if not squat_depth_check(right_angles, stop_ecc):
                                print("You need to squat deeper")

                            if not check_ratio_squats(right_angles):
                                print("slow down eccentric")
                                pass

                        """if not check_all_kneecaves(nframes, leftKnees, rightKnees, leftAnkles, rightAnkles):
                            print("You are caving your knees in, have them facing the same direction as your feet")"""


            if checkGoBack() == "true":
                break







        


            

