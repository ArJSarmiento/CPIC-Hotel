document.addEventListener('DOMContentLoaded', function() {
    let modal_form = document.getElementsByClassName("modal");
    let modal_data = document.getElementsByClassName("modalhidden");
    let checkInBtns = document.querySelectorAll(".checkInBtn")

    checkInBtns.forEach(function(btn) {
        btn.addEventListener("click", function() {
            let path = btn.dataset.path.toString();
            let data = btn.dataset.id.toString();
            let action = "/" + path ;
            modal_form[0].action = action;
            modal_data[0].value = data;
        })
    })
});