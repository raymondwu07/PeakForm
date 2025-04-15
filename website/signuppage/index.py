from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

#start web driver (chrome)
driver = webdriver.Chrome()
driver.get("http://127.0.0.1:5501/trainer/website/signuppage/index.html")

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "submitBtn")))


def setup_listener():
    driver.execute_script("""
        document.getElementById("submitBtn").addEventListener("click", () => {
            localStorage.setItem("clicked", "true");

            const emailVal = document.getElementById("loginEmail").value;
            const userVal = document.getElementById("loginUsername").value;
            const passVal = document.getElementById("loginPassword").value;

            localStorage.setItem("email", emailVal);
            localStorage.setItem("username", userVal);
            localStorage.setItem("password", passVal);
        });
    """)


def checkClicked():
    return driver.execute_script("return localStorage.getItem('clicked');")


def getEmail():
    return driver.execute_script("return localStorage.getItem('email');")

def getUsername():
    return driver.execute_script("return localStorage.getItem('username');")

def getPassword():
    return driver.execute_script("return localStorage.getItem('password');")

setup_listener()

while True:
    if checkClicked() == "true":

        if len(str(getUsername())) != 0:
            try:
                user_dir = f"/Users/raymondwu/codingprograms/trainer/website/database/{str(getUsername())}"
                if not os.path.isdir(user_dir):
                    os.mkdir(user_dir)

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
                                            signup.textContent = "Account Created!";""")
                    
                    except FileExistsError:
                        driver.execute_script("""
                                            const signup = document.getElementById("signupTxt");
                                            signup.textContent = "File already exists";""")
                
                else:
                    driver.execute_script("""
                                            const signup = document.getElementById("signupTxt");
                                            signup.textContent = "Username already exists";""")
            
            except Exception as e:
                print(f"Error creating directory: {e}")
                driver.execute_script("""
                                        const signup = document.getElementById("signupTxt");
                                        signup.textContent = "Username already exists";""")
            
            driver.execute_script("localStorage.setItem('clicked', 'false');")
        else:
            driver.execute_script("""
                                        const signup = document.getElementById("signupTxt");
                                        signup.textContent = "Enter a valid username please";""")

        #stops the script but keep the browser open
    time.sleep(1)

