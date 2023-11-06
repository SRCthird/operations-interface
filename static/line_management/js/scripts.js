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

const submitRejectForm = () => {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const line  = document.querySelector('input[name=line]').value;
    const employee = document.querySelector('input[name=employee]').value;
    const shift = document.querySelector('input[name=shift]').value;
    const workorder = document.querySelector('input[name=workorder]').value;
    const quantity = document.querySelector('input[name=quantity]').value;
    const reason = document.querySelector('select[name="reasons"]').value;
    const comments = document.querySelector('textarea[name="comments"]').value;
    
    const body = new URLSearchParams();
    body.append('line', line);
    body.append('line', line);
    body.append('line', line);
    body.append('line', line);
    body.append('line', line);
    body.append('line', line);
    body.append('line', line);


}
