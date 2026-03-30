function openPanel() {
    document.getElementById("loginPanel").classList.add("active");
    document.getElementById("overlay").style.display = "block";
}

function closePanel() {
    document.getElementById("loginPanel").classList.remove("active");
    document.getElementById("overlay").style.display = "none";
}