
const lineDown = document.getElementById('line-down');
const alert = document.getElementById('alert');
const killAlert = document.getElementById('kill-alert');

lineDown.addEventListener('click', () => {
    alert.style.display = 'block';
});

const kill_alert = () => {
    alert.style.display = 'none';
}