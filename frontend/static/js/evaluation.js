/**
 * Toggles the visibility of the input row in the evaluations table.
 */
function showEvaluationInputRow() {
    const evaluationInputRow = document.getElementById("evaluation-input-row");
    const showEvaluationButton = document.getElementById("show-evaluation-button");
    const addEvaluationButton = document.getElementById("add-evaluation-button");

    if (evaluationInputRow.style.display == "none") {
        evaluationInputRow.style.display = "table-row";
        showEvaluationButton.innerHTML = "-"
        addEvaluationButton.style.display = "block"
    } else {
        evaluationInputRow.style.display = "none";
        showEvaluationButton.innerHTML = "+"
        addEvaluationButton.style.display = "none"
    }
}

/**
 * Adds evaluation to the database and displays it in the evaluation table.
 *
 * @param {number} id The id of the course.
 */
async function addEvaluation(id) {
    try {
        const response = await fetch(
            `/evaluation`,
            {
                method: "POST",
                headers: new Headers({ "content-type": "application/json" }),
                body: JSON.stringify(
                    {
                        evaluation_name: document.getElementById("evaluation_name").value,
                        evaluation_grade: document.getElementById("evaluation_grade").value,
                        evaluation_weight: document.getElementById("evaluation_weight").value,
                        course_id: id
                    }
                )
            }
        );

        // If successful, display on the page
        if (response.status >= 200 && response.status < 300) {
            const evaluation = await response.json();

            // Get table
            const evaluationsTable = document.getElementById("evaluations-table");

            // Get the last row (input row)
            const inputRow = evaluationsTable.rows[evaluationsTable.rows.length - 1];

            // Create new table row
            const newEvaluationRow = document.createElement("tr");

            // Create cell for the evaluation name
            const nameCell = newEvaluationRow.insertCell();
            nameCell.appendChild(document.createTextNode(evaluation.evaluation_name));

            // Create cell for the evaluation grade
            const gradeCell = newEvaluationRow.insertCell();
            gradeCell.appendChild(document.createTextNode(`${evaluation.evaluation_grade * 100} %`));

            // Create cell for the evaluation weight
            const weightCell = newEvaluationRow.insertCell();
            weightCell.appendChild(document.createTextNode(`${evaluation.evaluation_weight * 100} %`));

            // Insert before the last row (input row)
            inputRow.parentElement.insertBefore(newEvaluationRow, inputRow);

            // Clear the inputs
            document.getElementById("evaluation_name").value = "";
            document.getElementById("evaluation_grade").value = "";
            document.getElementById("evaluation_weight").value = "";
        } else {
            alert("Didn't work sorry");
        }
    } catch (err) {
        alert(err.message);
    }
}
