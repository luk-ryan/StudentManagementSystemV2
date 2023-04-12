/**
 * Opens the add event modal.
 */
function openAddEventModal() {
    const addEventModal = document.getElementById("event-add-modal");
    addEventModal.style.display = "block";
}

/**
 * Closes the add course modal.
 */
function closeAddEventModal() {
    const addEventModal = document.getElementById("event-add-modal");
    addEventModal.style.display = "none";
}

window.onclick = function(event) {
    const addEventModal = document.getElementById("event-add-modal");
    if (event.target == addEventModal) {
        closeAddEventModal();
    }
}

/**
 * Adds evaluation to the database and displays it in the evaluation table.
 *
 * @param {number} studentId The id of the student.
 * @param {number} courseId The id of the course.
 */
function addEvent(studentId, courseId) {

}