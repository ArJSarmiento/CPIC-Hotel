document.addEventListener('DOMContentLoaded', function() {
    let input, filter,  li, a, i, txtValue;
    input = document.getElementById("myInput");
    li = document.getElementsByClassName("leaderboard__name");

    input.addEventListener("keyup", function() {
        filter = input.value.toUpperCase();
        for (i = 0; i < li.length; i++) {
            txtValue = li[i].textContent || li[i].innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                li[i].parentNode.style.display = "";
            } else {
                li[i].parentNode.style.display = "none";
            }
        }
    });
});