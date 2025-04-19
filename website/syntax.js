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