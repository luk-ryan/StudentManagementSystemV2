/**
 * Toggles the `hidden` property of the inputs and labels of a form.
 *
 * @param {HTMLElement} formElement The form to which the inputs and labels will be toggled.
 */
function toggleInputsAndLabels(formElement) {
    for (const child of formElement.children) {
        if (child.tagName.toUpperCase() == "LABEL" || child.tagName.toUpperCase() == "INPUT") {
            child.toggleAttribute("hidden");
        }
    }
}

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
 * Switches between the "previous" or "next" register page by toggling labels,
 * inputs, and buttons.
 *
 * On the first "page", the first set of inputs and labels are shown, along with
 * the next button. On the second "page", the second set of inputs are shown,
 * along with the previous and submit buttons. Toggling the `hidden` property of
 * these elements effectively switches between "pages".
 */
function switchRegisterPage() {
    const registerForm = document.getElementById("register-form");
    const toggleButton = document.getElementById("register-form-toggle-button");
    const submitButton = document.getElementById("register-form-submit-button");

    toggleInputsAndLabels(registerForm);

    toggleButton.innerHTML = toggleButton.innerHTML.toLowerCase() == "next"
        ? "Back"
        : "Next";

    submitButton.toggleAttribute("hidden");

    toggleButton.classList.toggle("shrink");
    submitButton.classList.toggle("shrink");
}

document.getElementById("register-form-toggle-button").addEventListener("click", switchRegisterPage);
