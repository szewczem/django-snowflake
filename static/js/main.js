// equipment_detail, account - alert //
const alertPlaceholder = document.getElementById('liveAlertPlaceholder')
const appendAlert = (message, type) => {
  const wrapper = document.createElement('div')
  wrapper.innerHTML = [
    `<div class="alert alert-${type} alert-dismissible" role="alert">`,
    `   <div>${message}</div>`,
    '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
    '</div>'
  ].join('')

  alertPlaceholder.append(wrapper)
}

const alertTrigger = document.getElementById('liveAlertBtn')
if (alertTrigger) {
  alertTrigger.addEventListener('click', () => {
    appendAlert('Reservation for {self.object.equipment.name} has been successfully deleted.', 'success')
  })
}


const modal = document.getElementById('exampleModal');

modal.addEventListener('show.bs.modal', function () {
  const detailStartDate = document.getElementById('detail-start-date').value;
  const detailEndDate = document.getElementById('detail-end-date').value;

  document.getElementById('reservation-start-date').value = detailStartDate;
  document.getElementById('reservation-end-date').value = detailEndDate;
});


// Checking phone number input in reservation form (equipment_detail)
document.addEventListener("DOMContentLoaded", function () {
  const phoneInput = document.getElementById("phoneNumber");
  const feedback = document.getElementById("phone-feedback");
  const reserveBtn = document.getElementById("ReserveBtn");

  // regex for numbers
  const phoneRegex = /^[0-9\s]{9}$/;

  phoneInput.addEventListener("input", function () {
      const isValid = phoneRegex.test(phoneInput.value);

      if (phoneInput.value === "") {
          phoneInput.classList.remove("is-valid", "is-invalid");
          feedback.classList.add("d-none");
      } else if (isValid) {
          phoneInput.classList.add("is-valid");
          phoneInput.classList.remove("is-invalid");
          feedback.classList.add("d-none");
          reserveBtn.classList.remove("disabled");
      } else {
          phoneInput.classList.add("is-invalid");
          phoneInput.classList.remove("is-valid");
          feedback.classList.remove("d-none");
          reserveBtn.classList.add("disabled");
      }
  });
});