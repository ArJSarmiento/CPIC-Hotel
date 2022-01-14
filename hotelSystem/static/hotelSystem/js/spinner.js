document.addEventListener('DOMContentLoaded', function() {
    let as = document.querySelectorAll('a');
    let spinner = document.querySelector('#spinner');
    spinner.style.display = 'none';
    for (let i = 0; i < as.length; i++) {
        as[i].addEventListener('click', function() {   
            document.activeElement.blur();
            if (spinner.style.display == 'none') {
                spinner.style.display = 'flex';
            }
            else {
                spinner.style.display = 'none';
            }
                
        });
    }
})