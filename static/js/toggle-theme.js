document.getElementById("darkSwitch").addEventListener("click", function(){
    document.getElementById("light-theme").style.display = "none";
    document.getElementById("dark-theme").style.display = "block";
    document.querySelector("body").style.backgroundColor = "#2c2c2c";
    document.querySelector(".loop-dir").style.color = "white";
    document.querySelector(".home_header").style.backgroundColor = "white";
});

document.getElementById("lightSwitch").addEventListener("click", function(){
    document.getElementById("light-theme").style.display = "block";
    document.getElementById("dark-theme").style.display = "none";
    document.querySelector("body").style.backgroundColor = "white";
    document.querySelector(".loop-dir").style.color = "black";
    document.querySelector(".home_header").style.backgroundColor = "black";
});