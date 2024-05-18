function openModal() {
    document.getElementById("deleteModal").style.display = "block";
}

function closeModal() {
    document.getElementById("deleteModal").style.display = "none";
}


window.onclick = function(event) {
    if (event.target == document.getElementById("deleteModal")) {
        closeModal();
    }
}