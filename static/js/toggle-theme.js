document.getElementById("darkSwitch").addEventListener("click", function(){
    document.getElementById("icon-dark").style.display = "none";
    document.getElementById("icon-light").style.display = "block";
    document.getElementById("body-theme").classList.toggle("bg-dark");
});

document.getElementById("lightSwitch").addEventListener("click", function(){
    document.getElementById("icon-dark").style.display = "block";
    document.getElementById("icon-light").style.display = "none";
    document.getElementById("body-theme").classList.toggle("bg-dark");
});