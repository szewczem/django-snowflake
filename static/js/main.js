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

// // getting dates from equipment_detail to modal
// const modal = document.getElementById('exampleModal');

// modal.addEventListener('show.bs.modal', function () {
//   const startDateInput = document.getElementById('reservation-start-date');
//   const endDateInput = document.getElementById('reservation-end-date');

//   const detailStartDate = document.getElementById('detail-start-date').value;
//   const detailEndDate = document.getElementById('detail-end-date').value;

//   if (!startDateInput.value) {
//     startDateInput.value = detailStartDate;
//   }
//   if (!endDateInput.value) {
//     endDateInput.value = detailEndDate;
//   }
// });


// Reservation form validation //
document.addEventListener("DOMContentLoaded", function () {
  const phoneInput = document.getElementById("phone-number");
  const startDateInput = document.getElementById("reservation-start-date");
  const endDateInput = document.getElementById("reservation-end-date");
  const checkbox = document.getElementById("check-agreement");
  const reserveBtn = document.getElementById("reserve-btn");

  const phoneFeedback = document.getElementById("phone-error");
  const dateError = document.getElementById("date-error");


  function setValid(input, feedback) {
    input.classList.add("is-valid");
    input.classList.remove("is-invalid");
    feedback.classList.add("d-none");
  }

  function setInvalid(input, feedback, message) {
    input.classList.add("is-invalid");
    input.classList.remove("is-valid");
    feedback.textContent = message;
    feedback.classList.remove("d-none");
  }

  // Phone number validation //
  const phoneRegex = /^[0-9]{9}$/;

  if(phoneInput.value) {
    validatePhoneInput();
  }

  // Full phone validation with feedback (only on blur)
  function validatePhoneInput() {
    const value = phoneInput.value;
    const isValid = phoneRegex.test(value);

    if (value === "") {
      phoneInput.classList.remove("is-valid", "is-invalid");
      phoneFeedback.classList.add("d-none");
    } else if (isValid) {
      setValid(phoneInput, phoneFeedback)
      return true;
    } else {
      setInvalid(phoneInput, phoneFeedback, 'Enter a valid 9-digit phone number.')
      return false;
    }
    return false;
  }

  // Allow only digits
  phoneInput.addEventListener("keypress", function (event) {
    if (!/^\d$/.test(event.key)) {
      event.preventDefault();
    }
  });

  // Handle paste for digits only
  phoneInput.addEventListener("paste", function (event) {
    event.preventDefault();
    const paste = event.clipboardData.getData("text");
    const digitsOnly = paste.replace(/\D/g, "");

    const currentValue = phoneInput.value;
    const selectionStart = phoneInput.selectionStart;
    const selectionEnd = phoneInput.selectionEnd;

    phoneInput.value =
      currentValue.slice(0, selectionStart) + digitsOnly + currentValue.slice(selectionEnd);

    const newCursorPos = selectionStart + digitsOnly.length;
    setTimeout(() => {
      phoneInput.setSelectionRange(newCursorPos, newCursorPos);
      validatePhoneInput();
      validateReservationForm();
    }, 0);
  });


  // Date fields validation //
  let wasEndDateFocused = false;

  endDateInput.addEventListener("focus", function () {
    wasEndDateFocused = true;
  });

  // Full date validation with feedback (used only on date inputs)
  function validateDateInputs() {
    const startDate = startDateInput.value;
    const endDate = endDateInput.value;

    startDateInput.classList.remove("is-valid", "is-invalid");
    endDateInput.classList.remove("is-valid", "is-invalid");
    dateError.classList.add("d-none");
    dateError.textContent = "";

    if (!startDate && endDate) {
      dateError.textContent = "Please fill out both start and end dates.";
      dateError.classList.remove("d-none");
      if (!startDate) startDateInput.classList.add("is-invalid");
      if (!endDate && wasEndDateFocused) endDateInput.classList.add("is-invalid");
      return false;
    } else if (startDate && !endDate && wasEndDateFocused) {
      setInvalid(endDateInput, dateError, "Please fill out both start and end dates.");
      return false;
    } else if (startDate && endDate) {
      const start = new Date(startDate);
      const end = new Date(endDate);
      if (end < start) {
        setInvalid(endDateInput, dateError, "End date must be after or the same as start date.");
        return false;
      } else {
        setValid(endDateInput, dateError);
        setValid(startDateInput, dateError);
        return true;
      }
    }
    return false;
  }

  if (startDateInput.value && endDateInput.value) {
    validateDateInputs();
  }

  // Enables or disables the Reserve button
  function validateReservationForm() {
    const isPhoneValid = validatePhoneInput();
    const isDateValid = validateDateInputs();
    const isChecked = checkbox.checked;

    if (isPhoneValid && isDateValid && isChecked) {
      reserveBtn.classList.remove("disabled");
    } else {
      reserveBtn.classList.add("disabled");
    }
  }

  // Validate phone input only on blur
  phoneInput.addEventListener("blur", function () {
    validatePhoneInput();
    validateReservationForm();
  });

  // Validate dates inputs
  startDateInput.addEventListener("input", function () {
    validateDateInputs();
    validateReservationForm();
  });

  endDateInput.addEventListener("input", function () {
    validateDateInputs();
    validateReservationForm();
  });

  // Checkbox change
  checkbox.addEventListener("change", validateReservationForm);
});