
const lineDown = document.getElementById('line-down');
const alert = document.getElementById('alert');

lineDown.addEventListener('click', () => {
    //alert.style.display = 'block';
});

const killAlert = () => {
    alert.style.display = 'none';
}

const showPopup = () => {
    document.getElementById("popupBackground").style.display = "flex";
}

const closePopup = () => {
    document.getElementById("popupBackground").style.display = "none";
}

const submitDowntimeForm = (button) => {
    const downtimeId = button.getAttribute('data-downtime-id');
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const employee = document.querySelector('input[name="employee"]').value;
    const reason = document.querySelector('select[name="reasons"]').value;
    const comments = document.querySelector('textarea[name="comments"]').value;

    const body = new URLSearchParams();
    body.append('employee', employee);
    body.append('reason', reason);
    body.append('comments', comments);

    fetch(`/operations/update_downtime/${downtimeId}/`, { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-CSRFToken': csrftoken,
        },
        body: body.toString(),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('Downtime updated successfully');
            killAlert();
            closePopup();
            location.reload()
        } else {
            console.log('Failed to update downtime');
        }
    })
    .catch(error => console.error('Error:', error));
}

const createDowntime = (button) => {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const employee = button.getAttribute('data-employee');
    const line = button.getAttribute('data-line');

    const body = new URLSearchParams();
    body.append('employee', employee);
    body.append('line', line);

    fetch(`/operations/create_downtime/`, { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-CSRFToken': csrfToken,
        },
        body: body.toString(),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('Downtime created successfully');
            location.reload()
        } else {
            console.log('Failed to create downtime');
            console.log(data.errors);
        }
    })
    .catch(error => console.error('Error:', error));
}

/**
 * 
 * @param {HTMLElement} field - The HTML element to be modified.
 * @param {string} endpoint - The server endpoint where the information will be fetched.
 */
const cascadingDropdown = (field, endpoint) => {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-CSRFToken': csrfToken,
        },
    })
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

            data.forEach(item => {
                const option = document.createElement("option");
                option.value = item.reason;
                option.textContent = item.reason;
                field.appendChild(option);
            });
        })
        .catch(error => {
            console.error("There was a problem with the fetch operation:", error.message);
        });
}

/**
 * The line is  from the dropdown, a request is sent to the server to retieve the corresponding part numbers.
 * 
 * @returns {void} - This function modifies the part number dropdown.
 */
const lineToReason = () => {
    /** The line to be selected */
    const line = document.querySelector('meta[name="line"]').getAttribute('content');

    /** The reasons dropdown to be modified */
    const reasons = document.getElementById("reasons");
    
    if (line && reasons) {
        const endpoint = `/operations/get_downtime_reasons/${line}`;
        cascadingDropdown(reasons, endpoint);
    } else {
        console.error("Fields not found");
        return;
    }
}

document.addEventListener("DOMContentLoaded", lineToReason);