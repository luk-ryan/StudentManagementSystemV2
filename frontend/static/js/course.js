

async function removeCourse(id) {
    await fetch(`/course/${id}`, {method:"DELETE"})
}