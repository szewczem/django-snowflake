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

//equipment_detail tooltip
document.addEventListener('DOMContentLoaded', function () {
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  tooltipTriggerList.forEach(function (tooltipTriggerEl) {
    new bootstrap.Tooltip(tooltipTriggerEl)
  })
})

// getting dates from equipment_detail to modal
const modal = document.getElementById('exampleModal');

modal.addEventListener('show.bs.modal', function () {
  const detailStartDate = document.getElementById('detail-start-date').value;
  const detailEndDate = document.getElementById('detail-end-date').value;

  document.getElementById('reservation-start-date').value = detailStartDate;
  document.getElementById('reservation-end-date').value = detailEndDate;
});


/// phone number validation, only digits ///
document.addEventListener("DOMContentLoaded", function () {
  const phoneInput = document.getElementById("phoneNumber");
  const feedback = document.getElementById("phone-feedback");
  const reserveBtn = document.getElementById("reserveBtn");

  if (!phoneInput) return;

  const phoneRegex = /^[0-9]{9}$/;

  // Validate input during typing
  function validatePhoneInput() {
    const value = phoneInput.value;
    const isValid = phoneRegex.test(value);

    if (value === "") {
      phoneInput.classList.remove("is-valid", "is-invalid");
      feedback.classList.add("d-none");
      reserveBtn.classList.add("disabled");
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
  }

  // Allow only digits during typing
  phoneInput.addEventListener("keypress", function (event) {
    if (!/^\d$/.test(event.key)) {
      event.preventDefault();
    }
  });

  // Clean pasted content and insert digits only
  phoneInput.addEventListener("paste", function (event) {
    event.preventDefault();
    const paste = event.clipboardData.getData("text");
    const digitsOnly = paste.replace(/\D/g, "");

    const currentValue = phoneInput.value;
    const selectionStart = phoneInput.selectionStart;
    const selectionEnd = phoneInput.selectionEnd;

    // Insert cleaned digits
    phoneInput.value =
      currentValue.slice(0, selectionStart) + digitsOnly + currentValue.slice(selectionEnd);

    // Move cursor after pasted content
    const newCursorPos = selectionStart + digitsOnly.length;
    setTimeout(() => {
      phoneInput.setSelectionRange(newCursorPos, newCursorPos);
      validatePhoneInput(); // Trigger validation after paste
    }, 0);
  });

  // Re-validate after change in input
  phoneInput.addEventListener("input", validatePhoneInput);
});
