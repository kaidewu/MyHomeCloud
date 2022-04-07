document.onkeydown = function(e){
    if (e.ctrlKey && (e.keyCode === 85)){
        return false;
    }
};