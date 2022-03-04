document.getElementById("upload-button").addEventListener("click", function(){
    document.querySelector(".upload-popup").style.display = "flex";
});

document.getElementById("upload-close").addEventListener("click", function(){
    document.querySelector(".upload-popup").style.display = "none";
});

document.getElementById("create-button").addEventListener("click", function(){
    document.querySelector(".create-popup").style.display = "flex";
});

document.getElementById("create-close").addEventListener("click", function(){
    document.querySelector(".create-popup").style.display = "none";
});