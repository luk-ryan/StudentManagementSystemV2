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
        } else {
            alert("Didn't work sorry");
        }
    } catch (err) {
        alert(err.message);
    }
}
