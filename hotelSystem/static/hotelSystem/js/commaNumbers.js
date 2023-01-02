document.addEventListener('DOMContentLoaded', function () {
    //add comma to numbers with more than 3 digits
    let numbers = document.querySelectorAll('.money');
    numbers.forEach(function (n) {
        n.innerHTML = n.innerHTML.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    });
});