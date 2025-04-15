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
driver.get("http://127.0.0.1:5501/trainer/website/loginpage/index.html")

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "submitBtn")))


def setup_listener():
    driver.execute_script("""
        document.getElementById("submitBtn").addEventListener("click", () => {
            localStorage.setItem("clicked", "true");

            const userVal = document.getElementById("loginUsername").value;
            const passVal = document.getElementById("loginPassword").value;

            localStorage.setItem("username", userVal);
            localStorage.setItem("password", passVal);
        });
    """)


def checkClicked():
    return driver.execute_script("return localStorage.getItem('clicked');")

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
                    driver.execute_script("""
                            const loginTxt = document.getElementbyId("loginTxt");
                            loginTxt.textContent = "Account doesn't exist"; """)
                else:
                    try:
                        user_file = f"/Users/raymondwu/codingprograms/trainer/website/database/{str(getUsername())}/{str(getUsername())}Info"
                        with open(user_file, "r") as file:
                            details = file.readline().split("|")
                        file.close()

                        if str(getUsername()) == details[1] and str(getPassword()) == details[2]:
                            driver.execute_script("""
                                window.location.href = "http://127.0.0.1:5501/trainer/website/training-log/index.html"; """)
                        else:
                            driver.execute_script("""
                            const loginTxt = document.getElementbyId("loginTxt");
                            loginTxt.textContent = "Incorrect username or password"; """)
                    except IOError:
                        driver.execute_script("""
                            const loginTxt = document.getElementbyId("loginTxt");
                            loginTxt.textContent = "file not found"; """)
            except Exception as e:
                print(f"Error creating directory: {e}")


        #stops the script but keep the browser open
    time.sleep(1)

