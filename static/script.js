const form = document.querySelector('form');
const responseDiv = document.getElementById('response');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData(form);
    const response = await fetch('/', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();
    responseDiv.textContent = JSON.stringify(data, null, 2);
});
