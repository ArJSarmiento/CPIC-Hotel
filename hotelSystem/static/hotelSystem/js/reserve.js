document.addEventListener('DOMContentLoaded', function() {

    const reserveSubmit = document.getElementById('reserveSubmit');
    const reserveInputs = document.querySelectorAll('#reserveField');
    const arrivalDateInput = document.querySelector('#arrivalDate #reserveField');
    const departureDateInput = document.querySelector('#departureDate #reserveField');
    let arrivalDate =0
    let departureDate = 0

    reserveSubmit.disabled=true;
    
    function disableButton(inputs, button) {
        for (let i = 0; i < inputs.length; i++) {
            if (inputs[i].value === '' || arrivalDate >= departureDate) {
                button.disabled = true;
                return;
            }
        }
        button.disabled = false;
    }

    reserveInputs.forEach(reserveInput => {
        reserveInput.addEventListener('keyup', ()  => {
            disableButton(reserveInputs, reserveSubmit);
        })
    });
    
    flatpickr(".datetimepicker-input", {
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        altInput: true,
        altFormat: "F j, Y H:i",
        minDate: "today",
        defaultDate: "today",
        defaultHour: "12",
        onChange: function(selectedDates, dateStr, instance) {
            if (selectedDates.length > 1) {
                instance.setDate(instance.latestSelectedDateObj.getTime() + (24 * 60 * 60 * 1000));
            }
            
            arrivalDate = new Date(arrivalDateInput.value);
            departureDate = new Date(departureDateInput.value);

            disableButton(reserveInputs, reserveSubmit)
        }
    });
})