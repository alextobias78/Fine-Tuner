const form = document.querySelector('form');
const responseDiv = document.getElementById('response');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData(form);
    const response = await fetch('/', {
        method: 'POST',
        body: formData
    });

    const text = await response.text();
    responseDiv.textContent = text;

    // Clear the user input and assistant input fields
    form.querySelector('#user_input').value = '';
    form.querySelector('#assistant_input').value = '';
});
