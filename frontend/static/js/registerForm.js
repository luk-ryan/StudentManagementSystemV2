/**
 * Toggles the `hidden` attribute of the register form buttons (previous page,
 * next page, and submit).
 */
function toggleRegisterFormButtons() {
    document.getElementById("register-form-back-button").toggleAttribute("hidden");
    document.getElementById("register-form-next-button").toggleAttribute("hidden");
    document.getElementById("register-form-submit-button").toggleAttribute("hidden");
}

/**
 * Switches between the "previous" or "next" register page by toggling between register forms page 1 and 2.
 * 
 * Also toggles 'Next' and 'Back' buttons.
 */
function switchRegisterPage() {
    const toggleButton = document.getElementById("register-form-toggle-button");
    const submitButton = document.getElementById("register-form-submit-button");

    document.getElementById("register-form-page-1").classList.toggle("hidden");
    document.getElementById("register-form-page-2").classList.toggle("hidden");

    toggleButton.innerHTML = toggleButton.innerHTML.toLowerCase() == "next"
        ? "Back"
        : "Next";

    submitButton.toggleAttribute("hidden");

    toggleButton.classList.toggle("shrink");
    submitButton.classList.toggle("shrink");
}

/**
 * Validates if any of the User's inputs are blank.
 * 
 * @param {HTMLElement} input User's input.
 * @returns {Boolean} returns true if user's input is not empty, otherwise false.
 */
function validateNotBlank(input) {
    return (input.value != "");
}

/**
 * Validates if the Register Form is filled in correctly, and if so, then submits the form,
 * otherwise, corresponding error messages will pop up.
 * 
 * The inputs for credits to graduate, first name, last name, email, and password 
 * are all required to be filled in.
 */
function validateAndSubmit() {

    let validated = true;

    const creditsToGraduate = document.getElementById("credits-to-graduate");
    const firstName = document.getElementById("first-name");
    const lastName = document.getElementById("last-name");
    const email = document.getElementById("email");
    const password = document.getElementById("password");

    const creditsToGraduateErrorMessage = creditsToGraduate.querySelector("p");
    const firstNameErrorMessage = firstName.querySelector("p");
    const lastNameErrorMessage = lastName.querySelector("p");
    const emailErrorMessage = email.querySelector("p");
    const passwordErrorMessage = password.querySelector("p");

    // validate Credits to Graduate
    if (!validateNotBlank(creditsToGraduate.querySelector("input"))) {
        creditsToGraduateErrorMessage.innerHTML = "Total Credits Required";
        creditsToGraduateErrorMessage.classList.remove("hidden")
        creditsToGraduate.querySelector("span").style.color = "var(--error-color)";
        validated = false;
    }
    else {
        creditsToGraduateErrorMessage.classList.add("hidden")
        creditsToGraduateErrorMessage.innerHTML = "";
        creditsToGraduate.querySelector("span").style.color = "var(--text-color)";
    }

    // validate First Name
    if (!validateNotBlank(firstName.querySelector("input"))) {
        firstNameErrorMessage.innerHTML = "First Name Required";
        firstNameErrorMessage.classList.remove("hidden")
        firstName.querySelector("span").style.color = "var(--error-color)";
        validated = false;
    }
    else {
        firstNameErrorMessage.classList.add("hidden")
        firstNameErrorMessage.innerHTML = "";
        firstName.querySelector("span").style.color = "var(--text-color)";
    }

    // validate Last Name
    if (!validateNotBlank(lastName.querySelector("input"))) {
        lastNameErrorMessage.innerHTML = "Last Name Required";
        lastNameErrorMessage.classList.remove("hidden")
        lastName.querySelector("span").style.color = "var(--error-color)";
        validated = false;
    }
    else {
        lastNameErrorMessage.classList.add("hidden")
        lastNameErrorMessage.innerHTML = "";
        lastName.querySelector("span").style.color = "var(--text-color)";
    }

    // validate Email
    if (!validateNotBlank(email.querySelector("input"))) {
        emailErrorMessage.innerHTML = "Email Required";
        emailErrorMessage.classList.remove("hidden")
        email.querySelector("span").style.color = "var(--error-color)";
        validated = false;
    }
    else {
        emailErrorMessage.classList.add("hidden")
        emailErrorMessage.innerHTML = "";
        email.querySelector("span").style.color = "var(--text-color)";
    }
    
    // Validate Password
    if (!validateNotBlank(password.querySelector("input"))) {
        passwordErrorMessage.innerHTML = "Password Required";
        passwordErrorMessage.classList.remove("hidden")
        password.querySelector("span").style.color = "var(--error-color)";
        validated = false;
    }
    else {
        passwordErrorMessage.classList.add("hidden")
        passwordErrorMessage.innerHTML = "";
        password.querySelector("span").style.color = "var(--text-color)";
    }

    if (validated) {
        document.getElementById("register-form").submit();
    }

}


document.getElementById("register-form-toggle-button").addEventListener("click", switchRegisterPage);
document.getElementById("register-form-submit-button").addEventListener("click", validateAndSubmit);
