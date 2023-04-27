/**
 * Removes a course from the database and from the page.
 *
 * @param {*} element The HTML element of the button being clicked.
 * @param {*} id The id of the course to delete.
 */
async function removeCourse(element, id) {
    try {
        // Delete the course in the database
        const response = await fetch(`/course/${id}`, { method:"DELETE" });

        if (response.status >= 200 && response.status < 300) {
            // Remove the course from the page
            element.parentElement.remove();
        } 
        else {
            alert("Didn't work sorry");
        }
    } 
    catch (err) {
        alert(err.message);
    }
}

/**
 * Opens the add course modal.
 */
function openAddCourseModal() {
    const addCourseModal = document.getElementById("course-add-modal");
    addCourseModal.style.display = "flex";
}

/**
 * Closes the add course modal.
 */
function closeAddCourseModal() {
    const addCourseModal = document.getElementById("course-add-modal");
    addCourseModal.style.display = "none";
}

window.addEventListener("click", function(event) {
    const addCourseModal = document.getElementById("course-add-modal");
    if (event.target == addCourseModal) {
        closeAddCourseModal();
    }
});

/**
 * Adds Semester to Student account
 */
async function addSemester() {
    const semesterForm = document.getElementById("form-add-semester");
    const errorMessage = document.getElementById("semester-add-modal-message");

    try {
        // Add Semester into Database
        const response = await fetch(`/semester`, { method:"POST", body: new FormData(semesterForm) });

        if (response.status >= 200 && response.status < 300) {
            const semester = await response.json();

            // Get semester dropdown
            const semesterDropdown = document.getElementById("semester-select-dropdown");

            // Create new option
            const newSemesterOption = document.createElement("option");

            newSemesterOption.setAttribute("value", semester.semester_id);
            newSemesterOption.appendChild(document.createTextNode(semester.semester_displayName));
            semesterDropdown.appendChild(newSemesterOption);

            // Clear the inputs
            semesterForm.querySelectorAll("input").forEach(input => input.value = "");
            errorMessage.innerHTML = "";
            errorMessage.style.display = "none";
            closeAddSemesterModal();
            document.getElementById("course-add-modal-message").style.display = "block";
            document.getElementById("course-add-modal-message").innerHTML = "Semester Added Successfully";
        }
        else {
            errorMessage.style.display = "block";
            errorMessage.innerHTML = await response.text();
        }
    } 
    catch (err) {
        errorMessage.style.display = "block";
        errorMessage.innerHTML = err.message;
    }
}

/**
 * Opens the add Semester modal.
 */
function openAddSemesterModal() {
    const addSemesterModal = document.getElementById("semester-add-modal");
    addSemesterModal.style.display = "flex";
}

/**
 * Closes the add Semester modal.
 */
function closeAddSemesterModal() {
    const addSemesterModal = document.getElementById("semester-add-modal");
    addSemesterModal.style.display = "none";
}

window.addEventListener("click", function(event) {
    const addSemesterModal = document.getElementById("semester-add-modal");
    if (event.target == addSemesterModal) {
        closeAddSemesterModal();
    }
});
