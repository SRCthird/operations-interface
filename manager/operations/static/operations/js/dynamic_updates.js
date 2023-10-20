/**
 * 
 * @param {HTMLElement} field - The HTML element to be modified.
 * @param {string} endpoint - The server endpoint where the information will be fetched.
 */
const cascadingDropdown = (field, endpoint) => {
    fetch(endpoint)
        .then(response => {
            if (response.status !== 200) {
                console.error("There was an error with the AJAX request.", response.status);
                return [];
            }
            return response.json();
        })
        .then(data => {
            while (field.firstChild) {
                field.firstChild.remove();
            }

            data.forEach(([value, label]) => {
                const option = document.createElement("option");
                option.value = value;
                option.textContent = label;
                field.appendChild(option);
            });
        })
        .catch(error => {
            console.error("There was a problem with the fetch operation:", error.message);
        });
}

/**
 * When the user slelects a workorder from the dropdown, a request is sent to the server to retieve the corresponding part numbers.
 * 
 * @returns {void} - This function modifies the part number dropdown.
 */
const workorderToPartNumber = () => {
    /** The workorder to be selected */
    const workorderField = document.getElementById("id_workorder");
    /** The part number dropdown to be modified */
    const partNumberField = document.getElementById("id_part_number");
    /** The server endpoint where the workorder will be sent */
    const endpoint = `/get_part_numbers/?workorder_id=${workorderField.value}`;

    workorderField.addEventListener("change", cascadingDropdown(partNumberField, endpoint));
}

document.addEventListener("DOMContentLoaded", workorderToPartNumber());
