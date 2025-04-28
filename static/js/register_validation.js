document.addEventListener("DOMContentLoaded", function () {
    const emailInput = document.getElementById("id_email");
    const nameInput = document.getElementById("id_username");
    const phoneInput = document.getElementById("id_phone_number");
    const password1Input = document.getElementById("id_password1");
    const password2Input = document.getElementById("id_password2");

    // display error messages
    function displayErrorMessage(message, field) {
        const errorDiv = document.getElementById(field + "-error-message");
        if (errorDiv) {
            errorDiv.textContent = message;
            errorDiv.classList.remove("d-none");
        }
    }    
    // clear error messages
    function clearErrorMessage(field) {
        const errorDiv = document.getElementById(field + "-error-message");
        if (errorDiv) {
            errorDiv.textContent = "";
            errorDiv.classList.add("d-none");
        }
    }

    // email validation
    if (emailInput) {
        emailInput.addEventListener("blur", function () {
            const email = emailInput.value.trim();
            console.log("Email input field lost focus", email);

            // Validate empty email
            if (!email) {
                emailInput.classList.add("is-invalid");
                emailInput.classList.remove("is-valid");
                displayErrorMessage("Email cannot be empty", "email");
                return;
            }

            // Validate email format
            const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
            if (!emailRegex.test(email)) {
                emailInput.classList.add("is-invalid");
                emailInput.classList.remove("is-valid");
                displayErrorMessage("Please enter a valid email (must contain '@' and a '.' after '@').", "email");
                return;
            }

            // Check email existence using AJAX
            checkEmail(email);
        });
        // AJAX validation, checking if provided email exist
        async function checkEmail(email) {
            try {
                const response = await fetch(`/users/ajax/check_email/?email=${encodeURIComponent(email)}`, {
                    method: "GET",
                });
                const data = await response.json();
            
                if (data.error) {
                    emailInput.classList.add("is-invalid");
                    emailInput.classList.remove("is-valid");
                    displayErrorMessage(data.error, "email");
                } else if (data.exists) {
                    emailInput.classList.add("is-invalid");
                    emailInput.classList.remove("is-valid");
                    displayErrorMessage("This email is already taken.", "email");
                } else {
                    emailInput.classList.add("is-valid");
                    emailInput.classList.remove("is-invalid");
                    clearErrorMessage("email");
                }
            } catch (error) {
                console.error("Error checking email:", error);
            }
        }
        // AJAX validation, checking if provided email exist
        // fetch(`/users/ajax/check_email/?email=${encodeURIComponent(email)}`, {
        //     method: "GET",
        // })
        // .then(response => response.json())
        // .then(data => {
        //     if (data.error) {
        //         emailInput.classList.add("is-invalid");
        //         emailInput.classList.remove("is-valid");
        //         displayErrorMessage(data.error, "email");
        //     } else if (data.exists) {
        //         emailInput.classList.add("is-invalid");
        //         emailInput.classList.remove("is-valid");
        //         displayErrorMessage("This email is already taken.", "email");
        //     } else {
        //         emailInput.classList.add("is-valid");
        //         emailInput.classList.remove("is-invalid");
        //         clearErrorMessage("email");
        //     }
        // })
        // .catch(error => {
        //     console.error("Error checking email:", error);
        // });
    } 
    
    // Name validation
    if (nameInput) {
        nameInput.addEventListener("blur", function () {
            const name = nameInput.value.trim();
            console.log("Name input field lost focus", name);

            // Check if name is not empty and has at least 3 characters
            if (!name) {
                nameInput.classList.add("is-invalid");
                nameInput.classList.remove("is-valid");
                displayErrorMessage("Name cannot be empty.", "name");
                return;
            } else if (name.length < 3) {
                nameInput.classList.add("is-invalid");
                nameInput.classList.remove("is-valid");
                displayErrorMessage("Name must be at least 3 characters long.", "name");
                return;
            } else {
                nameInput.classList.add("is-valid");
                nameInput.classList.remove("is-invalid");
                clearErrorMessage("name");
            }
        });
    }

    // Phone number validation
    if (phoneInput) {
        // only digitis durig typing
        phoneInput.addEventListener("keypress", function (event) {
            if (!/^\d$/.test(event.key)) {
                event.preventDefault();
            }
        });

        // paste only digits, set cursor position after pasted digits
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
            }, 0);
        });

        phoneInput.addEventListener("blur", function () {
            const phone = phoneInput.value.trim();
            console.log("Phone input field lost focus", phone);

            const phoneRegex = /^\d{9}$/; // Matches exactly 9 digits

            // Validate phone number (9 digits only)
            if (!phone) {
                phoneInput.classList.add("is-invalid");
                phoneInput.classList.remove("is-valid");
                displayErrorMessage("Phone number is required.", "phone");
                return;
            } else if (!phoneRegex.test(phone)) {
                phoneInput.classList.add("is-invalid");
                phoneInput.classList.remove("is-valid");
                displayErrorMessage("Phone number must be exactly 9 digits.", "phone");
                return;
            } else {
                phoneInput.classList.add("is-valid");
                phoneInput.classList.remove("is-invalid");
                clearErrorMessage("phone");
            }
        });
    }

    // Password validation
    if (password1Input && password2Input) {
        password1Input.addEventListener("blur", function () {
            const password1 = password1Input.value.trim();

            // Validate password1
            if (!password1) {
                password1Input.classList.add("is-invalid");
                password1Input.classList.remove("is-valid");
                displayErrorMessage("Password is required.", "password1");
                return;
            } else if (password1.length < 8) {
                password1Input.classList.add("is-invalid");
                password1Input.classList.remove("is-valid");
                displayErrorMessage("Password must be at least 8 characters long.", "password1");
                return;
            } else if (/\s/.test(password1)) {
                password1Input.classList.add("is-invalid");
                password1Input.classList.remove("is-valid");
                displayErrorMessage("Password cannot contain spaces.", "password1");
                return;
            } else {
                checkPassword(password1);
            }
        });

        password2Input.addEventListener("blur", function () {
            const password1 = password1Input.value.trim();
            const password2 = password2Input.value.trim();

            if (password1.length >= 8) {
                if (password2 === "") {
                    password2Input.classList.add("is-invalid");
                    password2Input.classList.remove("is-valid");
                    displayErrorMessage("Please confirm your password.", "password2");
                } else if (password2 !== password1) {
                    password2Input.classList.add("is-invalid");
                    password2Input.classList.remove("is-valid");
                    displayErrorMessage("The two password fields didn’t match.", "password2");
                } else {
                    password2Input.classList.add("is-valid");
                    password2Input.classList.remove("is-invalid");
                    clearErrorMessage("password2");
                }
            } else {
                password2Input.classList.remove("is-valid");
                password2Input.classList.remove("is-invalid");
                clearErrorMessage("password2");
            }
        });
        // AJAX checking password for too common (rejected by django)
        async function checkPassword(password) {
            try {
                const response = await fetch(`/users/ajax/check_password/?password=${encodeURIComponent(password)}`, {
                    method: "GET",
                });
                const data = await response.json();
                
                if (data.valid) {
                    password1Input.classList.add("is-valid");
                    password1Input.classList.remove("is-invalid");
                    clearErrorMessage("password1");
                } else {
                    password1Input.classList.add("is-invalid");
                    password1Input.classList.remove("is-valid");
                    displayErrorMessage(data.errors.join(' '), "password1");
                }
            } catch (error) {
                console.error("Error checking password:", error);
            }
        }
    }   
});

